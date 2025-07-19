import sys

from PyQt6.QtWidgets import QApplication

from app import __version__, __appname__, __desktopid__
from app.settings.app_settings import AppSettings
from app.themes.theme_provider import configure_theme
from app.views.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName(__appname__)
    app.setDesktopFileName(__desktopid__)

    app_settings = AppSettings()
    window = MainWindow(app_settings)
    configure_theme(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
