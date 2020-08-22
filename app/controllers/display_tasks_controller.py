from app.data.entities import TaskState
from app.views.display_tasks_view import DisplayTasksView


class DisplayTasksController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.view = DisplayTasksView(parent)

        # domain events
        self.app.data.app_events.task_updated.connect(self.refresh)

    def init(self):
        self.refresh()

    def on_task_added(self, task_id):
        task_entity = self.app.data.get_task_entity(task_id)
        self.view.render_task_entity(task_entity, self.on_task_done)

    def on_task_done(self, task_id):
        task_entity = self.app.data.get_task_entity(task_id)
        task_entity.mark_as_done()
        self.app.data.update_task(task_entity)

    def refresh(self):
        self.view.clear()
        task_entities = self.app.data.get_tasks(str(TaskState.NEW))
        for task_entity in task_entities:
            self.view.render_task_entity(task_entity, self.on_task_done)
