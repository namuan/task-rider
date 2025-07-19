from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QShortcut


class ShortcutController:
    def __init__(self, parent_window, app):
        self.parent = parent_window
        self.app = app

    def init_items(self):
        toggle_timer = QShortcut(QKeySequence("Ctrl+S"), self.parent)
        toggle_timer.activated.connect(self.parent.manage_timer_controller.toggle_timer)
        reset_timer = QShortcut(QKeySequence("Ctrl+R"), self.parent)
        reset_timer.activated.connect(self.parent.manage_timer_controller.reset_timer)
        add_task = QShortcut(QKeySequence("Ctrl+Return"), self.parent)
        add_task.activated.connect(self.parent.add_task_controller.add_task)
        new_task = QShortcut(QKeySequence("Ctrl+N"), self.parent)
        new_task.activated.connect(self.parent.add_task_controller.prepare_entry)
        config = QShortcut(QKeySequence("Ctrl+,"), self.parent)
        config.activated.connect(self.parent.config_controller.show_dialog)
