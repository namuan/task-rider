from app.data.entities import TaskEntity, TaskState
from app.utils.uuid_utils import gen_uuid


class AddTaskController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # ui events
        self.parent.btn_add_task.pressed.connect(self.add_task)
        self.parent.txt_task_title.returnPressed.connect(self.parent.btn_add_task.click)

    def add_task(self):
        task_id = gen_uuid()
        task_title = self.parent.txt_task_title.text()
        if task_title.strip():
            last_new_task = self.app.data.get_last_task(TaskState.NEW)
            task = TaskEntity(
                id=task_id,
                task_title=task_title,
                order=last_new_task.order + 1 if last_new_task else 1,
            )
            self.app.data.update_task(task)
            self.parent.txt_task_title.clear()

    def prepare_entry(self):
        self.parent.txt_task_title.setFocus()
