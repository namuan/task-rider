from PyQt6 import QtWidgets

from app.data.entities import TaskState
from app.views.display_tasks_view import DisplayTasksView


class DisplayTasksController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.view = DisplayTasksView(parent)
        self.view.setup_context_menu(on_delete_selected=self.on_delete_selected_item)
        self.view.setup_item_edit_handler(on_edit_selected=self.on_edit_task)

        # ui events
        self.parent.lst_tasks.setDragDropMode(
            QtWidgets.QAbstractItemView.DragDropMode.NoDragDrop
        )
        self.parent.lst_tasks.model().rowsMoved.connect(self.after_drop)

        # domain events
        self.app.data.app_events.task_updated.connect(self.refresh)
        self.app.data.app_events.config_changed.connect(self.update_snooze_tooltips)

    def init(self):
        self.refresh()

    def on_edit_task(self, item_widget):
        self.view.show_task_editor(item_widget)

    def on_delete_selected_item(self):
        task_id = self.view.selected_task_widget()
        if task_id:
            self.app.data.delete_task(task_id)

    def after_drop(self):
        self.refresh()

    def on_task_done(self, task_id):
        self.app.data.set_completed(task_id, True)

    def on_task_reopen(self, task_id):
        self.app.data.set_completed(task_id, False)

    def on_task_save(self, task_id, new_task_title):
        self.app.data.update_title(task_id, new_task_title)

    def on_task_snooze(self, task_id):
        self.app.data.snooze_task(task_id, hours=int(self.app.snooze_hours()))

    def refresh(self):
        self.view.clear()
        task_entities = self.app.data.get_tasks(TaskState.NEW)
        for task_entity in task_entities:
            task_widget = self.view.render_task_entity(
                task_entity, self.on_task_done, self.on_task_save, self.on_task_snooze
            )
            if task_widget and hasattr(task_widget, "set_snooze_hours"):
                task_widget.set_snooze_hours(self.app.snooze_hours())
        completed_task_entities = self.app.data.get_tasks(
            TaskState.DONE, 5, "-done_time"
        )
        for task_entity in completed_task_entities:
            self.view.render_completed_task_entity(task_entity, self.on_task_reopen)

    def update_snooze_tooltips(self):
        for _, task_widget in self.view.widget_iterator():
            if task_widget and hasattr(task_widget, "set_snooze_hours"):
                task_widget.set_snooze_hours(self.app.snooze_hours())
