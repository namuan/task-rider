from PyQt5 import QtWidgets

from app.generated.TaskItemWidget_ui import Ui_TaskItemWidget


class TaskItemWidget(QtWidgets.QWidget, Ui_TaskItemWidget):
    def __init__(self, parent=None, on_btn_new_item_pressed=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setLayout(self.horizontalLayout)
        if on_btn_new_item_pressed:
            self.btn_new_item.pressed.connect(on_btn_new_item_pressed)

    def set_data(self, task_entity):
        self.txt_task_title.setText(task_entity.task_title)