from functools import partial

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFontMetrics

from app.generated.CompletedTaskItemWidget_ui import Ui_CompletedTaskItemWidget


class CompletedTaskItemWidget(QtWidgets.QWidget, Ui_CompletedTaskItemWidget):
    def __init__(self, parent, task_entity, on_btn_task_reopen_pressed=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        self.btn_task_reopen.setIcon(QIcon("images:done-48.png"))
        self.task_entity = task_entity
        self.full_task_title = task_entity.task_title
        self.lbl_task_title.setText(self.task_entity.task_title)
        self.lbl_task_title.setToolTip(self.task_entity.task_title)
        self.update_elided_text()
        if on_btn_task_reopen_pressed:
            self.btn_task_reopen.pressed.connect(
                partial(
                    on_btn_task_reopen_pressed,
                    self.task_entity.id,
                )
            )

    def update_elided_text(self):
        font_metrics = QFontMetrics(self.lbl_task_title.font())
        available_width = self.lbl_task_title.width()
        elided_text = font_metrics.elidedText(
            self.full_task_title, Qt.TextElideMode.ElideRight, available_width
        )
        self.lbl_task_title.setText(elided_text)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_elided_text()

    def get_task_id(self):
        return self.task_entity.id

    def edit_task(self):
        pass
