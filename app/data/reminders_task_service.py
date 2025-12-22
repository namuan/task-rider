import logging
from datetime import datetime, timedelta
from typing import Callable
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from app.data.entities import TaskEntity, TaskState
from app.events.signals import AppEvents


class RemindersTaskService:
    def __init__(self):
        self.app_events = AppEvents()
        self._permission_prompt_handler: Optional[Callable[[str], None]] = None

        self._remind_kit = None
        self._default_calendar_id: Optional[str] = None

        self._incomplete_tasks: list[TaskEntity] = []
        self._recent_completed_tasks: list[TaskEntity] = []

    def set_permission_prompt_handler(
        self, handler: Optional[Callable[[str], None]]
    ) -> None:
        self._permission_prompt_handler = handler

    def ensure_access(self) -> bool:
        if self._remind_kit and self._default_calendar_id:
            return True

        try:
            from pyremindkit import RemindKit

            self._remind_kit = RemindKit()
            default_calendar = self._remind_kit.calendars.get_default()
            self._default_calendar_id = getattr(default_calendar, "id", None)
            if not self._default_calendar_id:
                raise RuntimeError("No default Reminders list available")
            return True
        except Exception as e:
            self._remind_kit = None
            self._default_calendar_id = None
            err_str = str(e).lower()
            if (
                "unauthor" in err_str or "access" in err_str or "permission" in err_str
            ) and self._permission_prompt_handler:
                self._permission_prompt_handler(str(e))
            else:
                logging.exception("Failed to initialize RemindKit")
            return False

    def refresh(self) -> None:
        if not self.ensure_access():
            self._incomplete_tasks = []
            self._recent_completed_tasks = []
            self.app_events.task_updated.emit("")
            return

        try:
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            reminders_incomplete = self._get_calendar_reminders(
                is_completed=False, due_before=tomorrow
            )
        except Exception:
            logging.exception("Failed to fetch reminders")
            self._incomplete_tasks = []
            self._recent_completed_tasks = []
            self.app_events.task_updated.emit("")
            return

        incomplete_tasks = []
        for reminder in reminders_incomplete:
            task = self._task_from_reminder(reminder)
            if task:
                incomplete_tasks.append(task)

        incomplete_tasks.sort(key=self._task_sort_key)

        self._incomplete_tasks = incomplete_tasks
        self._recent_completed_tasks = []
        self.app_events.task_updated.emit("")

    def list_incomplete_and_recently_completed(
        self, completed_limit: int = 5
    ) -> Tuple[Sequence[TaskEntity], Sequence[TaskEntity]]:
        return self._incomplete_tasks, self._recent_completed_tasks[:completed_limit]

    def create_task(self, title: str, due: Optional[datetime] = None) -> None:
        if not title.strip():
            return
        if not self.ensure_access():
            return

        try:
            kwargs = {"title": title.strip(), "calendar_id": self._default_calendar_id}
            if due:
                kwargs["due_date"] = due
            try:
                self._remind_kit.create_reminder(**kwargs)
            except TypeError:
                kwargs.pop("due_date", None)
                self._remind_kit.create_reminder(**kwargs)
        except Exception:
            logging.exception("Failed to create reminder")
            return

        self.refresh()

    def update_title(self, reminder_id: str, title: str) -> None:
        if not reminder_id:
            return
        if not self.ensure_access():
            return

        try:
            self._remind_kit.update_reminder(reminder_id, title=title)
        except Exception:
            logging.exception("Failed to update reminder title")
            return

        self.refresh()

    def set_completed(self, reminder_id: str, completed: bool) -> None:
        if not reminder_id:
            return
        if not self.ensure_access():
            return

        try:
            self._remind_kit.update_reminder(reminder_id, is_completed=bool(completed))
        except Exception:
            logging.exception("Failed to update reminder completion")
            return

        self.refresh()

    def snooze_task(self, reminder_id: str, hours: int = 6) -> None:
        """Snooze a task by updating its due date to now + specified hours."""
        if not reminder_id:
            return
        if not self.ensure_access():
            return

        current_time = datetime.now()
        new_due_date = current_time + timedelta(hours=hours)

        try:
            reminder = None
            get_reminder_by_id = getattr(self._remind_kit, "get_reminder_by_id", None)
            if callable(get_reminder_by_id):
                try:
                    reminder = get_reminder_by_id(reminder_id)
                except Exception:
                    reminder = None

            due_date = self._reminder_due_date(reminder) if reminder else None
            is_past_event = bool(due_date and due_date < current_time)

            if is_past_event and reminder:
                calendar_id = getattr(reminder, "calendar_id", None)
                if not calendar_id:
                    calendar_obj = getattr(reminder, "calendar", None)
                    calendar_id = getattr(calendar_obj, "id", None)
                if not calendar_id:
                    calendar_id = self._default_calendar_id

                title = (
                    getattr(reminder, "title", None) or ""
                ).strip() or "Untitled reminder"
                kwargs = {"title": title, "calendar_id": calendar_id}
                notes = getattr(reminder, "notes", None)
                if notes:
                    kwargs["notes"] = notes
                priority = getattr(reminder, "priority", None)
                if priority is not None:
                    kwargs["priority"] = priority
                kwargs["due_date"] = new_due_date

                try:
                    self._remind_kit.create_reminder(**kwargs)
                except TypeError:
                    kwargs.pop("due_date", None)
                    self._remind_kit.create_reminder(**kwargs)

                try:
                    self._remind_kit.delete_reminder(reminder_id)
                except Exception:
                    logging.exception("Failed to delete original reminder after snooze")
                    try:
                        self._remind_kit.update_reminder(reminder_id, is_completed=True)
                    except Exception:
                        logging.exception(
                            "Failed to complete original reminder after failed delete"
                        )
            else:
                self._remind_kit.update_reminder(reminder_id, due_date=new_due_date)
        except Exception:
            logging.exception("Failed to snooze reminder")
            return

        self.refresh()

    def delete_task(self, reminder_id: str) -> None:
        if not reminder_id:
            return
        if not self.ensure_access():
            return

        try:
            self._remind_kit.delete_reminder(reminder_id)
        except Exception:
            logging.exception("Failed to delete reminder")
            return

        self.refresh()

    def get_tasks(self, task_state: TaskState, limit: int = 100, sort_key: str = ""):
        if task_state == TaskState.NEW:
            return list(self._incomplete_tasks)[:limit]
        if task_state == TaskState.DONE:
            return list(self._recent_completed_tasks)[:limit]
        return []

    def get_task_entity(self, task_id: str) -> Optional[TaskEntity]:
        if not task_id:
            return None
        for task in self._incomplete_tasks:
            if task.id == task_id:
                return task
        for task in self._recent_completed_tasks:
            if task.id == task_id:
                return task
        return None

    def get_task_entity_by_reminder_id(self, reminder_id: str) -> Optional[TaskEntity]:
        return self.get_task_entity(reminder_id)

    def get_top_task(self) -> Optional[TaskEntity]:
        return self._incomplete_tasks[0] if self._incomplete_tasks else None

    def get_last_task(self, task_state: TaskState) -> Optional[TaskEntity]:
        tasks = self.get_tasks(task_state, limit=1_000_000)
        return tasks[-1] if tasks else None

    def update_many_tasks(self, task_entities: Sequence[TaskEntity]) -> None:
        self.refresh()

    def _get_calendar_reminders(
        self, is_completed: bool, due_before: Optional[datetime] = None
    ) -> Sequence[object]:
        get_reminders = getattr(self._remind_kit, "get_reminders", None)
        if not callable(get_reminders):
            return []

        base_filter = {
            "calendar_id": self._default_calendar_id,
            "is_completed": is_completed,
        }
        if due_before:
            base_filter["due_before"] = due_before

        candidates: list[dict[str, object]] = [
            base_filter,
            dict(base_filter, **{"is_completed": is_completed}),
            {"calendar_id": self._default_calendar_id, "completed": is_completed},
            (
                {"is_completed": is_completed, "due_before": due_before}
                if due_before
                else {"is_completed": is_completed}
            ),
            (
                {"completed": is_completed, "due_before": due_before}
                if due_before
                else {"completed": is_completed}
            ),
            {},
        ]

        reminders, _ = self._try_get_reminders(get_reminders, candidates)
        if not reminders:
            return []

        filtered = []
        for r in reminders:
            reminder_calendar_id = getattr(r, "calendar_id", None)
            if not reminder_calendar_id:
                calendar_obj = getattr(r, "calendar", None)
                reminder_calendar_id = getattr(calendar_obj, "id", None)
            if (
                self._default_calendar_id
                and reminder_calendar_id
                and str(reminder_calendar_id) != str(self._default_calendar_id)
            ):
                continue
            if due_before:
                due_date = self._reminder_due_date(r)
                if due_date and due_date >= due_before:
                    continue
            if bool(getattr(r, "is_completed", False)) == bool(is_completed):
                filtered.append(r)
        return filtered

    def _try_get_reminders(
        self, get_reminders, kwargs_candidates: list[dict[str, object]]
    ) -> Tuple[list[object], dict[str, object]]:
        for kwargs in kwargs_candidates:
            try:
                return list(get_reminders(**kwargs)), kwargs
            except TypeError:
                continue
        return [], {}

    def _task_from_reminder(self, reminder) -> Optional[TaskEntity]:
        reminder_id = getattr(reminder, "id", None)
        if not reminder_id:
            return None

        title = (getattr(reminder, "title", None) or "").strip() or "Untitled reminder"
        is_completed = bool(getattr(reminder, "is_completed", False))
        due_date = self._reminder_due_date(reminder)
        completed_at = self._reminder_completed_at(reminder)

        task = TaskEntity(
            id=str(reminder_id),
            task_title=title,
            reminder_id=str(reminder_id),
            due_date=due_date,
        )
        if is_completed:
            task.mark_as_done()
            if completed_at:
                task.done_time = completed_at
        else:
            task.task_state = TaskState.NEW
            task.done_time = None
        return task

    def _task_sort_key(self, task: TaskEntity):
        due_ts = self._dt_to_sortable_ts(getattr(task, "due_date", None))
        title = (getattr(task, "task_title", None) or "").casefold()
        reminder_id = (
            getattr(task, "reminder_id", None) or getattr(task, "id", "") or ""
        )
        if due_ts is None:
            return (1, 0, title, reminder_id)
        return (0, due_ts, title, reminder_id)

    def _completed_sort_key(self, task: TaskEntity):
        done_ts = self._dt_to_sortable_ts(getattr(task, "done_time", None))
        due_ts = self._dt_to_sortable_ts(getattr(task, "due_date", None))
        title = (getattr(task, "task_title", None) or "").casefold()
        reminder_id = (
            getattr(task, "reminder_id", None) or getattr(task, "id", "") or ""
        )
        return (done_ts or -1, due_ts or -1, title, reminder_id)

    def _dt_to_sortable_ts(self, dt: Optional[datetime]) -> Optional[float]:
        if not isinstance(dt, datetime):
            return None
        try:
            return dt.timestamp()
        except Exception:
            return None

    def _reminder_due_date(self, reminder) -> Optional[datetime]:
        due_date: Union[None, str, datetime] = getattr(reminder, "due_date", None)
        if isinstance(due_date, datetime):
            return due_date
        if isinstance(due_date, str):
            try:
                return datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None

    def _reminder_completed_at(self, reminder) -> Optional[datetime]:
        candidates = [
            getattr(reminder, "completed_at", None),
            getattr(reminder, "completion_date", None),
            getattr(reminder, "completed_date", None),
            getattr(reminder, "completion_time", None),
        ]
        for value in candidates:
            if isinstance(value, datetime):
                return value
            if isinstance(value, str):
                try:
                    return datetime.fromisoformat(value.replace("Z", "+00:00"))
                except ValueError:
                    continue
        return None
