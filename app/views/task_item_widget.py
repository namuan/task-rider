from functools import partial

from PyQt5 import QtWidgets

from app.data.entities import TaskState
from app.generated.TaskItemWidget_ui import Ui_TaskItemWidget


class TaskItemWidget(QtWidgets.QWidget, Ui_TaskItemWidget):
    def __init__(self, parent, task_entity, on_btn_task_done_pressed=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.task_entity = task_entity
        if on_btn_task_done_pressed:
            self.btn_task_done.pressed.connect(
                partial(on_btn_task_done_pressed, self.task_entity.id, )
            )

        self.txt_task_title.setText(self.task_entity.task_title)
        if self.task_entity.task_state == TaskState.DONE:
            self.btn_task_done.hide()
            self.txt_task_title.setReadOnly(True)
