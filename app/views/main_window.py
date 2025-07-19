import logging
import traceback

import sys
from PyQt6 import QtCore
from PyQt6.QtGui import QCloseEvent, QIcon
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget

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
from app.settings.app_settings import AppSettings


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self, app_settings: AppSettings):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.app_settings = app_settings
        self.setupUi(self)

        self.btn_add_task.setIcon(QIcon(":images/add-48.png"))
        self.btn_toggle_timer.setIcon(QIcon(":images/start-48.png"))
        self.btn_reset_timer.setIcon(QIcon(":images/reset-48.png"))

        # Initialise controllers
        self.main_controller = MainWindowController(self, app_settings)
        self.config_controller = ConfigController(self, app_settings)
        self.shortcut_controller = ShortcutController(self, app_settings)
        self.add_task_controller = AddTaskController(self, app_settings)
        self.display_tasks_controller = DisplayTasksController(self, app_settings)
        self.manage_timer_controller = ManageTimerController(self, app_settings)
        self.overlay_controller = OverlayController(self, app_settings)
        self.time_report_controller = TimeReportController(self, app_settings)
        self.refresh_screen_controller = RefreshScreenController(self, app_settings)

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
            QApplication.instance().exit(0)
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
