import logging
import os
import sys
from datetime import datetime, timedelta

from PyQt6.QtCore import QUrl as QtQUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QMessageBox

from app.data.entities import TaskEntity, TaskState
from app.utils.uuid_utils import gen_uuid


class RemindersController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.remind_kit = None
        self.default_calendar_id = None
        self._suppressed_task_ids: set[str] = set()

        self.app.data.app_events.task_updated.connect(self.on_task_updated)

    def init(self):
        if not self.ensure_remindkit():
            return
        self.refresh_from_apple_reminders()
        self.sync_missing_reminders()

    def ensure_remindkit(self) -> bool:
        if self.remind_kit and self.default_calendar_id:
            return True

        try:
            from pyremindkit import RemindKit

            self.remind_kit = RemindKit()
            default_calendar = self.remind_kit.calendars.get_default()
            self.default_calendar_id = getattr(default_calendar, "id", None)
            if not self.default_calendar_id:
                raise RuntimeError("No default Reminders list available")
            return True
        except Exception as e:
            self.remind_kit = None
            self.default_calendar_id = None
            err_str = str(e).lower()
            if "unauthor" in err_str or "access" in err_str or "permission" in err_str:
                self.prompt_for_reminders_permission(error_message=str(e))
            else:
                logging.exception("Failed to initialize RemindKit")
            return False

    def prompt_for_reminders_permission(self, error_message: str = ""):
        title = "Reminders Permission Required"
        body = (
            "Task Rider needs permission to access Apple Reminders.\n\n"
            "Allow Reminders access in System Settings, then restart Task Rider.\n\n"
            "Error details:\n" + (error_message or "<no details>")
        )

        msg = QMessageBox(self.parent)
        msg.setWindowTitle(title)
        msg.setText(body)
        msg.setIcon(QMessageBox.Icon.Warning)
        open_button = msg.addButton("Open Settings", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Dismiss", QMessageBox.ButtonRole.RejectRole)
        msg.setDefaultButton(open_button)
        msg.exec()

        if msg.clickedButton() == open_button:
            self.open_reminders_privacy_settings()

    def open_reminders_privacy_settings(self):
        try:
            if sys.platform == "darwin":
                url = "x-apple.systempreferences:com.apple.preference.security?Privacy_Reminders"
                if not QDesktopServices.openUrl(QtQUrl(url)):
                    QDesktopServices.openUrl(
                        QtQUrl(
                            "x-apple.systempreferences:com.apple.preference.security"
                        )
                    )
            elif sys.platform == "win32":
                os.system("start ms-settings:privacy")
            else:
                QDesktopServices.openUrl(QtQUrl("about:blank"))
        except Exception:
            logging.exception("Failed to open system settings")

    def on_task_updated(self, task_id: str):
        if task_id in self._suppressed_task_ids:
            return
        task_entity = self.app.data.get_task_entity(task_id)
        if not task_entity:
            return
        self.sync_task(task_entity)

    def sync_missing_reminders(self):
        for task_entity in self.app.data.get_tasks(TaskState.NEW):
            if not getattr(task_entity, "reminder_id", None):
                self.sync_task(task_entity)

    def refresh_from_apple_reminders(self):
        if not self.ensure_remindkit():
            return

        try:
            reminders = self._get_default_calendar_reminders()
        except Exception:
            logging.exception("Failed to fetch reminders")
            return

        updated_count = 0
        created_count = 0

        for reminder in reminders:
            reminder_id = getattr(reminder, "id", None)
            title = (getattr(reminder, "title", None) or "").strip()
            is_completed = bool(getattr(reminder, "is_completed", False))
            notes = getattr(reminder, "notes", None) or ""

            task_entity = None
            if reminder_id:
                task_entity = self.app.data.get_task_entity_by_reminder_id(reminder_id)

            notes_task_id = self._task_id_from_notes(notes)
            if not task_entity and notes_task_id:
                task_entity = self.app.data.get_task_entity(notes_task_id)

            if task_entity:
                changed = False
                if (
                    reminder_id
                    and getattr(task_entity, "reminder_id", None) != reminder_id
                ):
                    task_entity.reminder_id = reminder_id
                    changed = True

                if title and task_entity.task_title != title:
                    task_entity.task_title = title
                    changed = True

                current_state = self._normalize_task_state(
                    getattr(task_entity, "task_state", None)
                )
                desired_state = TaskState.DONE if is_completed else TaskState.NEW
                if current_state != desired_state:
                    if desired_state == TaskState.DONE:
                        task_entity.mark_as_done()
                    else:
                        task_entity.mark_as_new()
                    changed = True

                if changed:
                    self._suppressed_task_ids.add(task_entity.id)
                    try:
                        self.app.data.update_task(task_entity)
                    finally:
                        self._suppressed_task_ids.discard(task_entity.id)
                    updated_count += 1
                continue

            if not reminder_id:
                continue

            task_id = gen_uuid()
            task_title = title or "Untitled reminder"
            last_new_task = self.app.data.get_last_task(TaskState.NEW)
            task_entity = TaskEntity(
                id=task_id,
                task_title=task_title,
                reminder_id=reminder_id,
                order=last_new_task.order + 1 if last_new_task else 1,
            )
            if is_completed:
                task_entity.mark_as_done()

            self._suppressed_task_ids.add(task_entity.id)
            try:
                self.app.data.update_task(task_entity)
            finally:
                self._suppressed_task_ids.discard(task_entity.id)
            created_count += 1

        logging.info(
            "Refreshed reminders from Apple Reminders. Updated: %s, Created: %s",
            updated_count,
            created_count,
        )

    def sync_task(self, task_entity):
        if not self.ensure_remindkit():
            return

        state = self._normalize_task_state(getattr(task_entity, "task_state", None))

        reminder_id = getattr(task_entity, "reminder_id", None)
        if not reminder_id and state in {TaskState.NEW, TaskState.DONE}:
            created = self.remind_kit.create_reminder(
                title=task_entity.task_title,
                notes=f"task-rider:{task_entity.id}",
                calendar_id=self.default_calendar_id,
            )
            reminder_id = getattr(created, "id", None)
            if reminder_id:
                self._update_task_reminder_id(task_entity, reminder_id)

        if not reminder_id:
            return

        if state == TaskState.NEW:
            self.remind_kit.update_reminder(
                reminder_id,
                title=task_entity.task_title,
                is_completed=False,
            )
        elif state == TaskState.DONE:
            self.remind_kit.update_reminder(
                reminder_id,
                title=task_entity.task_title,
                is_completed=True,
            )
        elif state == TaskState.DELETED:
            self.remind_kit.delete_reminder(reminder_id)

    def _update_task_reminder_id(self, task_entity, reminder_id: str):
        if getattr(task_entity, "reminder_id", None) == reminder_id:
            return
        task_entity.reminder_id = reminder_id
        self._suppressed_task_ids.add(task_entity.id)
        try:
            self.app.data.update_task(task_entity)
        finally:
            self._suppressed_task_ids.discard(task_entity.id)

    def _normalize_task_state(self, task_state):
        if isinstance(task_state, TaskState):
            return task_state
        if isinstance(task_state, str):
            name = task_state.split(".")[-1]
            return TaskState[name] if name in TaskState.__members__ else None
        return None

    def _try_get_reminders(
        self, get_reminders, kwargs_candidates: list[dict[str, object]]
    ):
        for kwargs in kwargs_candidates:
            try:
                return list(get_reminders(**kwargs)), kwargs
            except TypeError:
                continue
        return [], {}

    def _get_default_calendar_reminders(self):
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        reminders = list(
            self.remind_kit.get_reminders(due_before=tomorrow, is_completed=False)
        )
        logging.info(f"Found {len(reminders)} incomplete reminders due before tomorrow")
        return reminders

    def _task_id_from_notes(self, notes: str) -> str | None:
        prefix = "task-rider:"
        if not isinstance(notes, str):
            return None
        for line in notes.splitlines():
            line = line.strip()
            if line.startswith(prefix):
                return line.removeprefix(prefix).strip() or None
        return None

    def _reminder_due_date(self, reminder) -> datetime | None:
        due_date = getattr(reminder, "due_date", None)
        if isinstance(due_date, datetime):
            return due_date
        if isinstance(due_date, str):
            try:
                return datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None
