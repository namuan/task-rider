from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from app.generated.CompletedTaskItemWidget_ui import Ui_CompletedTaskItemWidget


class CompletedTaskItemWidget(QtWidgets.QWidget, Ui_CompletedTaskItemWidget):
    def __init__(self, parent, task_entity, on_btn_task_reopen_pressed=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.btn_task_reopen.setIcon(QIcon(":images/done-48.png"))
        self.task_entity = task_entity
        self.lbl_task_title.setText(self.task_entity.task_title)
        self.lbl_task_title.setToolTip(self.task_entity.task_title)
        if on_btn_task_reopen_pressed:
            self.btn_task_reopen.pressed.connect(
                partial(on_btn_task_reopen_pressed, self.task_entity.id, )
            )
