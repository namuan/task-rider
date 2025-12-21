import logging
import os
import sys

from PyQt6.QtCore import QUrl as QtQUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QMessageBox


class RemindersController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

    def init(self):
        self.app.data.set_permission_prompt_handler(
            self.prompt_for_reminders_permission
        )
        self.app.data.refresh()

    def prompt_for_reminders_permission(self, error_message: str = ""):
        title = "Reminders Permission Required"
        body = (
            "Task Rider needs permission to access Apple Reminders.\n\n"
            "Allow Reminders access in System Settings, then restart Task Rider.\n\n"
            "Error details:\n" + (error_message or "<no details>")
        )

        msg = QMessageBox(self.parent)
        msg.setWindowTitle(title)
        msg.setText(body)
        msg.setIcon(QMessageBox.Icon.Warning)
        open_button = msg.addButton("Open Settings", QMessageBox.ButtonRole.AcceptRole)
        msg.addButton("Dismiss", QMessageBox.ButtonRole.RejectRole)
        msg.setDefaultButton(open_button)
        msg.exec()

        if msg.clickedButton() == open_button:
            self.open_reminders_privacy_settings()

    def open_reminders_privacy_settings(self):
        try:
            if sys.platform == "darwin":
                url = "x-apple.systempreferences:com.apple.preference.security?Privacy_Reminders"
                if not QDesktopServices.openUrl(QtQUrl(url)):
                    QDesktopServices.openUrl(
                        QtQUrl(
                            "x-apple.systempreferences:com.apple.preference.security"
                        )
                    )
            elif sys.platform == "win32":
                os.system("start ms-settings:privacy")
            else:
                QDesktopServices.openUrl(QtQUrl("about:blank"))
        except Exception:
            logging.exception("Failed to open system settings")

    def refresh_from_apple_reminders(self):
        self.app.data.refresh()
