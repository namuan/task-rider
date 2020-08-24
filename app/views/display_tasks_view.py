import logging

from PyQt5 import QtWidgets

from app.views.completed_task_item_widget import CompletedTaskItemWidget
from app.views.task_item_widget import TaskItemWidget


class DisplayTasksView:
    def __init__(self, main_window):
        self.main_window = main_window

    def clear(self):
        self.main_window.lst_tasks.clear()

    def render_task_entity(self, task_entity, callback=None):
        logging.info("Adding a new task widget for {}".format(task_entity))
        task_widget = TaskItemWidget(
            self.main_window, task_entity, callback
        )

        task_widget_item = QtWidgets.QListWidgetItem(self.main_window.lst_tasks)
        task_widget_item.setSizeHint(task_widget.sizeHint())

        self.main_window.lst_tasks.addItem(task_widget_item)
        self.main_window.lst_tasks.setItemWidget(task_widget_item, task_widget)

    def render_completed_task_entity(self, task_entity):
        logging.info("Adding a new completed task widget for {}".format(task_entity))
        task_widget = CompletedTaskItemWidget(
            self.main_window, task_entity
        )

        task_widget_item = QtWidgets.QListWidgetItem(self.main_window.lst_tasks)
        task_widget_item.setSizeHint(task_widget.sizeHint())

        self.main_window.lst_tasks.addItem(task_widget_item)
        self.main_window.lst_tasks.setItemWidget(task_widget_item, task_widget)