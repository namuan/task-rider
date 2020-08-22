from app.views.display_tasks_view import DisplayTasksView


class DisplayTasksController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.view = DisplayTasksView(parent)

        # domain events
        self.app.data.app_events.task_added.connect(self.on_task_added)

    def init(self):
        # Todo: Load and display all tasks
        pass

    def on_task_added(self, task_id):
        task_entity = self.app.data.get_task_entity(task_id)
        self.view.render_task_entity(task_entity)
