import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from app import __version__, __appname__, __desktopid__
from app.settings.app_settings import AppSettings
from app.themes.theme_provider import configure_theme
from app.views.main_window import MainWindow

from PyQt6.QtCore import QDir



def main():
    app = QApplication(sys.argv)
    app.setApplicationVersion(__version__)
    app.setApplicationName(__appname__)
    app.setDesktopFileName(__desktopid__)

    resources_path = (Path(__file__).parent.parent / "resources")

    QDir.addSearchPath('themes', resources_path.joinpath("themes").as_posix())
    QDir.addSearchPath('images', resources_path.joinpath("images").as_posix())
    QDir.addSearchPath('fonts', resources_path.joinpath("fonts").as_posix())
    QDir.addSearchPath('icons', resources_path.joinpath("icons").as_posix())
    QDir.addSearchPath('sounds', resources_path.joinpath("sounds").as_posix())

    app_settings = AppSettings()
    window = MainWindow(app_settings)
    configure_theme(app)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
