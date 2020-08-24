from app.data.entities import TaskEntity
from app.utils.uuid_utils import gen_uuid


class AddTaskController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # ui events
        self.parent.btn_add_task.pressed.connect(self.add_task)

    def add_task(self):
        task_id = gen_uuid()
        task_title = self.parent.txt_task_title.text()
        task = TaskEntity(id=task_id, task_title=task_title)
        self.app.data.update_task(task)
        self.parent.txt_task_title.clear()
