from functools import partial

from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon

from app.generated.CompletedTaskItemWidget_ui import Ui_CompletedTaskItemWidget
from app.widgets.task_item_widget import BaseTaskItemWidget


class CompletedTaskItemWidget(BaseTaskItemWidget, Ui_CompletedTaskItemWidget):
    MIN_ITEM_HEIGHT = 56

    def __init__(self, parent, task_entity, on_btn_task_reopen_pressed=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.setMinimumHeight(self.MIN_ITEM_HEIGHT)

        self.horizontalLayout.setStretch(1, 1)
        self.lbl_task_title.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )

        self.btn_task_reopen.setIcon(QIcon("images:done-48.png"))
        self.task_entity = task_entity
        self.init_elided_title(self.task_entity.task_title)
        if on_btn_task_reopen_pressed:
            self.btn_task_reopen.pressed.connect(
                partial(
                    on_btn_task_reopen_pressed,
                    self.task_entity.id,
                )
            )

    def get_task_id(self):
        return self.task_entity.id

    def edit_task(self):
        pass
