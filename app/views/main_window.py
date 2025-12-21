import logging
import traceback

import sys
from PyQt6 import QtCore
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QAction, QCloseEvent, QDesktopServices, QIcon, QKeySequence
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
    RemindersController,
)
from app.generated.MainWindow_ui import Ui_MainWindow
from app.settings.app_settings import AppSettings


class MainWindow(QMainWindow, Ui_MainWindow):
    """Main Window."""

    def __init__(self, app_settings: AppSettings):
        QMainWindow.__init__(self, None, QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.app_settings = app_settings
        self.setupUi(self)

        self.btn_add_task.setIcon(QIcon("images:add-48.png"))
        self.btn_toggle_timer.setIcon(QIcon("images:start-48.png"))
        self.btn_reset_timer.setIcon(QIcon("images:reset-48.png"))

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
        self.reminders_controller = RemindersController(self, app_settings)

        # Initialise components
        self.shortcut_controller.init_items()

        # Initialise Sub-Systems
        sys.excepthook = MainWindow.log_uncaught_exceptions
        self._init_menu_bar()

    def _init_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        refresh_reminders_action = QAction(
            "Refresh reminders from Apple Reminders", self
        )
        refresh_reminders_action.setShortcut(QKeySequence("Ctrl+Shift+R"))
        refresh_reminders_action.triggered.connect(
            self.reminders_controller.refresh_from_apple_reminders
        )
        file_menu.addAction(refresh_reminders_action)

        open_logs_action = QAction("Open logs directory", self)
        open_logs_action.triggered.connect(self.open_logs_directory)
        file_menu.addAction(open_logs_action)

    def open_logs_directory(self):
        logs_dir = getattr(self.app_settings, "app_dir", None)
        if not logs_dir:
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(logs_dir.as_posix()))

    # Main Window events
    def resizeEvent(self, event):
        self.overlay_controller.resize(event.size())
        self.main_controller.after_window_loaded()

    def updateScreen(self):
        QWidget.repaint(self)

    @staticmethod
    def log_uncaught_exceptions(cls, exc, tb) -> None:
        logging.critical("".join(traceback.format_tb(tb)))
        logging.critical("{}: {}".format(cls, exc))

    def closeEvent(self, event: QCloseEvent):
        logging.info("Received close event")
        event.accept()
        self.main_controller.shutdown()
        try:
            QApplication.instance().exit(0)
        except Exception:
            pass

    def replace_widget(self, selected_widget):
        self.clear_layout(self.toolWidgetLayout)
        self.toolWidgetLayout.addWidget(selected_widget)

    def clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            widget_item = layout.takeAt(i)
            if widget_item:
                widget_item.widget().deleteLater()
