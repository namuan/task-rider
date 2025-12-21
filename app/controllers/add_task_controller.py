class AddTaskController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # ui events
        self.parent.btn_add_task.pressed.connect(self.add_task)
        self.parent.txt_task_title.returnPressed.connect(self.parent.btn_add_task.click)

    def add_task(self):
        task_title = self.parent.txt_task_title.text()
        if task_title.strip():
            self.app.data.create_task(task_title)
            self.parent.txt_task_title.clear()

    def prepare_entry(self):
        self.parent.txt_task_title.setFocus()
