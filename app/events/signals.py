from PyQt5.QtCore import QObject, pyqtSignal


class AppEvents(QObject):
    task_updated = pyqtSignal(str)
    config_changed = pyqtSignal()


class AppCommands(QObject):
    pass
