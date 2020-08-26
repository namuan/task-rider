import logging

from PyQt5 import QtWidgets

from app.widgets.completed_task_item_widget import CompletedTaskItemWidget
from app.widgets.task_item_widget import TaskItemWidget


class DisplayTasksView:
    def __init__(self, main_window):
        self.main_window = main_window

    def clear(self):
        self.main_window.lst_tasks.clear()

    def widget_iterator(self):
        for i in range(self.main_window.lst_tasks.count()):
            task_widget = self.main_window.lst_tasks.itemWidget(
                self.main_window.lst_tasks.item(i)
            )
            yield i, task_widget

    def render_task_entity(self, task_entity, callback=None):
        logging.info("Adding a new task widget for {}".format(task_entity))
        task_widget = TaskItemWidget(self.main_window, task_entity, callback)

        task_widget_item = QtWidgets.QListWidgetItem(self.main_window.lst_tasks)
        task_widget_item.setSizeHint(task_widget.sizeHint())

        self.main_window.lst_tasks.addItem(task_widget_item)
        self.main_window.lst_tasks.setItemWidget(task_widget_item, task_widget)

    def render_completed_task_entity(self, task_entity, callback=None):
        logging.info("Adding a new completed task widget for {}".format(task_entity))
        task_widget = CompletedTaskItemWidget(self.main_window, task_entity, callback)

        task_widget_item = QtWidgets.QListWidgetItem(self.main_window.lst_tasks)
        task_widget_item.setSizeHint(task_widget.sizeHint())

        self.main_window.lst_tasks.addItem(task_widget_item)
        self.main_window.lst_tasks.setItemWidget(task_widget_item, task_widget)
