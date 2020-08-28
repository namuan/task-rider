from PyQt5.QtCore import QObject, pyqtSignal


class AppEvents(QObject):
    task_updated = pyqtSignal(str)
    time_report_updated = pyqtSignal(str)
    config_changed = pyqtSignal()
    timer_started = pyqtSignal()
    timer_paused = pyqtSignal()


class AppCommands(QObject):
    pass
