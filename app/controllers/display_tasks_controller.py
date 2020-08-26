from app.data.entities import TaskState, TaskEntity
from app.views.display_tasks_view import DisplayTasksView


class DisplayTasksController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.view = DisplayTasksView(parent)

        # ui events
        self.parent.lst_tasks.model().rowsMoved.connect(self.after_drop)

        # domain events
        self.app.data.app_events.task_updated.connect(self.refresh)

    def init(self):
        self.refresh()

    def after_drop(self):
        task_entities = [
            self.task_entity_with_position(pos, t.get_task_id()) for pos, t in self.view.widget_iterator()
        ]
        self.app.data.update_many_tasks(task_entities)

    def task_entity_with_position(self, position, task_id):
        task_entity: TaskEntity = self.app.data.get_task_entity(task_id)
        task_entity.order = position
        return task_entity

    def on_task_done(self, task_id):
        task_entity = self.app.data.get_task_entity(task_id)
        task_entity.mark_as_done()
        self.app.data.update_task(task_entity)

    def on_task_reopen(self, task_id):
        task_entity = self.app.data.get_task_entity(task_id)
        task_entity.mark_as_new()
        self.app.data.update_task(task_entity)

    def refresh(self):
        self.view.clear()
        task_entities = self.app.data.get_tasks(str(TaskState.NEW))
        for task_entity in task_entities:
            self.view.render_task_entity(task_entity, self.on_task_done)
        completed_task_entities = self.app.data.get_tasks(str(TaskState.DONE), 5)
        for task_entity in completed_task_entities:
            self.view.render_completed_task_entity(task_entity, self.on_task_reopen)
