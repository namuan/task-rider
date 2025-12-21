import logging
import logging.handlers
from pathlib import Path
from typing import Any, Union

from PyQt6.QtCore import QSettings, QStandardPaths
from PyQt6.QtWidgets import QApplication

from app.data import RemindersTaskService
from app.settings.app_config import AppConfig


class AppSettings:
    def __init__(self):
        self.settings: QSettings = QSettings()
        self.app_name: str = QApplication.instance().applicationName()
        self.app_dir: Union[Path, Any] = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppConfigLocation
            )
        )

        self.docs_location: Path = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.DocumentsLocation
            )
        )
        self.data: RemindersTaskService = None

    def init(self):
        self.app_name = QApplication.instance().applicationName().lower()
        self.app_dir = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppConfigLocation
            )
        )
        self.app_dir.mkdir(exist_ok=True)
        settings_file = f"{self.app_name}.ini"
        self.settings = QSettings(
            self.app_dir.joinpath(settings_file).as_posix(), QSettings.Format.IniFormat
        )
        self.settings.sync()
        self.data = RemindersTaskService()

    def init_logger(self):
        log_file = f"{self.app_name}.log"
        handlers = [
            logging.handlers.RotatingFileHandler(
                self.app_dir.joinpath(log_file), maxBytes=1000000, backupCount=1
            ),
            logging.StreamHandler(),
        ]

        logging.basicConfig(
            handlers=handlers,
            format="%(asctime)s - %(filename)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.DEBUG,
        )
        logging.captureWarnings(capture=True)

    def save_window_state(self, geometry, window_state):
        self.settings.setValue("geometry", geometry)
        self.settings.setValue("windowState", window_state)
        self.settings.sync()

    def save_configuration(self, app_config: AppConfig):
        self.settings.setValue(AppConfig.TIMER_VALUE, app_config.timer_value)
        self.settings.sync()
        self.data.app_events.config_changed.emit()

    def load_configuration(self):
        app_config = AppConfig()
        app_config.timer_value = self.settings.value(
            AppConfig.TIMER_VALUE, app_config.timer_value
        )
        return app_config

    def geometry(self):
        return self.settings.value("geometry", None)

    def window_state(self):
        return self.settings.value("windowState", None)

    def timer_value(self):
        app_config = self.load_configuration()
        return app_config.timer_value
