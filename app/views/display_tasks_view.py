import logging

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QMenu, QAction

from app.widgets.completed_task_item_widget import CompletedTaskItemWidget
from app.widgets.task_item_widget import TaskItemWidget


class DisplayTasksView:
    def __init__(self, main_window):
        self.main_window = main_window

    def setup_item_edit_handler(self, on_edit_selected):
        self.main_window.lst_tasks.itemDoubleClicked.connect(on_edit_selected)

    def setup_context_menu(self, on_delete_selected):
        delete_action = QAction("Delete", self.main_window.lst_tasks)
        delete_action.triggered.connect(on_delete_selected)

        self.menu = QMenu()
        self.menu.addAction(delete_action)

        self.main_window.lst_tasks.setContextMenuPolicy(Qt.CustomContextMenu)
        self.main_window.lst_tasks.customContextMenuRequested.connect(
            self.on_display_context_menu
        )

    def on_display_context_menu(self, position):
        index: QModelIndex = self.main_window.lst_tasks.indexAt(position)
        if not index.isValid():
            return

        global_position = self.main_window.lst_tasks.viewport().mapToGlobal(position)
        self.menu.exec_(global_position)

    def clear(self):
        self.main_window.lst_tasks.clear()

    def task_from_widget(self, item_widget):
        return self.main_window.lst_tasks.itemWidget(item_widget)

    def selected_task_widget(self):
        item_widget = self.main_window.lst_tasks.currentItem()
        if item_widget:
            t = self.task_from_widget(item_widget)
            return t.get_task_id()
        else:
            return None

    def widget_iterator(self):
        for i in range(self.main_window.lst_tasks.count()):
            task_widget = self.task_from_widget(self.main_window.lst_tasks.item(i))
            yield i, task_widget

    def show_task_editor(self, item_widget):
        task_widget = self.task_from_widget(item_widget)
        task_widget.edit_task()

    def render_task_entity(self, task_entity, on_btn_task_done=None, on_task_save=None):
        logging.info("Adding a new task widget for {}".format(task_entity))
        task_widget = TaskItemWidget(
            self.main_window, task_entity, on_btn_task_done, on_task_save
        )

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
