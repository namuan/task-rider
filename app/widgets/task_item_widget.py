from functools import partial
from datetime import datetime, timedelta

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, QEvent, Qt
from PyQt6.QtGui import QIcon, QFontMetrics

from app.generated.TaskItemWidget_ui import Ui_TaskItemWidget


class LineEditorEvents(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def eventFilter(self, source: QObject, event: QEvent):
        if (
            event.type() == QtCore.QEvent.Type.KeyPress
            and event.key() == QtCore.Qt.Key.Key_Escape
        ):
            self.parent.dismiss_editor()

        return super().eventFilter(source, event)


class TaskItemWidget(QtWidgets.QWidget, Ui_TaskItemWidget):
    MIN_ITEM_HEIGHT = 72

    def __init__(
        self,
        parent,
        task_entity,
        on_task_done_handler=None,
        on_task_save_handler=None,
        on_task_snooze_handler=None,
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.setMinimumHeight(self.MIN_ITEM_HEIGHT)
        self.txt_task_title.hide()
        self.btn_task_done.setIcon(QIcon("images:new-48.png"))
        self.btn_snooze.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed
        )
        self.btn_snooze.setFixedSize(26, 26)
        snooze_font = self.btn_snooze.font()
        snooze_font.setPointSize(max(8, snooze_font.pointSize() - 1))
        self.btn_snooze.setFont(snooze_font)

        self.task_entity = task_entity
        self.full_task_title = task_entity.task_title
        self.on_task_save_handler = on_task_save_handler

        self.events = LineEditorEvents(self)
        self.txt_task_title.installEventFilter(self.events)

        if on_task_done_handler:
            self.btn_task_done.pressed.connect(
                partial(
                    on_task_done_handler,
                    self.task_entity.id,
                )
            )

        if on_task_snooze_handler and self.task_entity.due_date:
            self.btn_snooze.pressed.connect(
                partial(
                    on_task_snooze_handler,
                    self.task_entity.id,
                )
            )
        else:
            self.btn_snooze.hide()

        self.txt_task_title.returnPressed.connect(self.on_save_task)
        self.lbl_task_title.setText(self.task_entity.task_title)
        self.lbl_task_title.setToolTip(self.task_entity.task_title)
        self.update_elided_text()
        self.update_due_date_text()

    def sizeHint(self):
        hint = super().sizeHint()
        return QtCore.QSize(hint.width(), max(hint.height(), self.minimumHeight()))

    def minimumSizeHint(self):
        hint = super().minimumSizeHint()
        return QtCore.QSize(hint.width(), max(hint.height(), self.minimumHeight()))

    def set_snooze_hours(self, hours: int) -> None:
        try:
            hours_int = int(hours)
        except Exception:
            hours_int = 6
        unit = "hour" if hours_int == 1 else "hours"
        self.btn_snooze.setToolTip(f"Snooze for {hours_int} {unit}")

    def get_task_id(self):
        return self.task_entity.id

    def edit_task(self):
        self.lbl_task_title.hide()
        self.txt_task_title.setText(self.task_entity.task_title)
        self.txt_task_title.show()

    def dismiss_editor(self):
        self.txt_task_title.hide()
        self.lbl_task_title.show()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_elided_text()

    def on_save_task(self):
        self.on_task_save_handler(self.task_entity.id, self.txt_task_title.text())
        self.full_task_title = self.txt_task_title.text()
        self.update_elided_text()

    def update_elided_text(self):
        font_metrics = QFontMetrics(self.lbl_task_title.font())
        available_width = self.lbl_task_title.width()
        elided_text = font_metrics.elidedText(
            self.full_task_title, Qt.TextElideMode.ElideRight, available_width
        )
        self.lbl_task_title.setText(elided_text)

    def update_due_date_text(self):
        if not self.task_entity.due_date:
            self.lbl_due_date.hide()
            return

        due_date = self.task_entity.due_date
        now = datetime.now()

        # Check if the due date is in the past
        is_overdue = due_date < now

        # Format the due date in a subtle, readable way
        if due_date.date() == now.date():
            # Today - show time
            due_text = f"Due today at {due_date.strftime('%H:%M')}"
        elif due_date.date() == (now + timedelta(days=1)).date():
            # Tomorrow - show time
            due_text = f"Due tomorrow at {due_date.strftime('%H:%M')}"
        elif not is_overdue and (due_date - now).days < 7:
            # Within a week - show day name and time
            due_text = f"Due {due_date.strftime('%A at %H:%M')}"
        else:
            # Further away or past due - show date and time
            due_text = f"Due {due_date.strftime('%b %d at %H:%M')}"

        self.lbl_due_date.setText(due_text)
        self.lbl_due_date.show()
