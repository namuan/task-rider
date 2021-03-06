import logging
import traceback

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import QMainWindow, qApp, QWidget

from app.controllers import (
    MainWindowController,
    ConfigController,
    ShortcutController,
    AddTaskController,
    DisplayTasksController,
    ManageTimerController,
    OverlayController,
    TimeReportController,
    RefreshScreenController,
)
from app.generated.MainWindow_ui import Ui_MainWindow
from app.settings.app_settings import app


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.btn_add_task.setIcon(QIcon(":images/add-48.png"))
        self.btn_toggle_timer.setIcon(QIcon(":images/start-48.png"))
        self.btn_reset_timer.setIcon(QIcon(":images/reset-48.png"))

        # Initialise controllers
        self.main_controller = MainWindowController(self, app)
        self.config_controller = ConfigController(self, app)
        self.shortcut_controller = ShortcutController(self, app)
        self.add_task_controller = AddTaskController(self, app)
        self.display_tasks_controller = DisplayTasksController(self, app)
        self.manage_timer_controller = ManageTimerController(self, app)
        self.overlay_controller = OverlayController(self, app)
        self.time_report_controller = TimeReportController(self, app)
        self.refresh_screen_controller = RefreshScreenController(self, app)

        # Initialise components
        self.shortcut_controller.init_items()

        # Initialise Sub-Systems
        sys.excepthook = MainWindow.log_uncaught_exceptions

    # Main Window events
    def resizeEvent(self, event):
        self.overlay_controller.resize(event.size())
        self.main_controller.after_window_loaded()

    def updateScreen(self):
        QWidget.repaint(self)

    @staticmethod
    def log_uncaught_exceptions(cls, exc, tb) -> None:
        logging.critical("".join(traceback.format_tb(tb)))
        logging.critical("{0}: {1}".format(cls, exc))

    def closeEvent(self, event: QCloseEvent):
        logging.info("Received close event")
        event.accept()
        self.main_controller.shutdown()
        try:
            qApp.exit(0)
        except:
            pass

    def replace_widget(self, selected_widget):
        self.clear_layout(self.toolWidgetLayout)
        self.toolWidgetLayout.addWidget(selected_widget)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget_item = layout.takeAt(i)
            if widget_item:
                widget_item.widget().deleteLater()
