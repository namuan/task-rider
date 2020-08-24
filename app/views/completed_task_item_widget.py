from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from app.generated.CompletedTaskItemWidget_ui import Ui_CompletedTaskItemWidget


class CompletedTaskItemWidget(QtWidgets.QWidget, Ui_CompletedTaskItemWidget):
    def __init__(self, parent, task_entity):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.btn_task_done.setIcon(QIcon(":images/done-48.png"))
        self.task_entity = task_entity
        self.lbl_task_title.setText(self.task_entity.task_title)
        self.lbl_task_title.setToolTip(self.task_entity.task_title)
