from PyQt5.QtCore import QObject, pyqtSignal


class AppEvents(QObject):
    task_updated = pyqtSignal(str)


class AppCommands(QObject):
    pass
