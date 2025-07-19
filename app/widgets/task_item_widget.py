from functools import partial

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtGui import QIcon

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
    def __init__(
        self, parent, task_entity, on_task_done_handler=None, on_task_save_handler=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.txt_task_title.hide()
        self.btn_task_done.setIcon(QIcon("images:new-48.png"))

        self.task_entity = task_entity
        self.on_task_save_handler = on_task_save_handler

        self.events = LineEditorEvents(self)
        self.txt_task_title.installEventFilter(self.events)

        if on_task_done_handler:
            self.btn_task_done.pressed.connect(
                partial(on_task_done_handler, self.task_entity.id,)
            )

        self.txt_task_title.returnPressed.connect(self.on_save_task)
        self.lbl_task_title.setText(self.task_entity.task_title)
        self.lbl_task_title.setToolTip(self.task_entity.task_title)

    def on_save_task(self):
        self.on_task_save_handler(self.task_entity.id, self.txt_task_title.text())

    def get_task_id(self):
        return self.task_entity.id

    def edit_task(self):
        self.lbl_task_title.hide()
        self.txt_task_title.setText(self.task_entity.task_title)
        self.txt_task_title.show()

    def dismiss_editor(self):
        self.txt_task_title.hide()
        self.lbl_task_title.show()
