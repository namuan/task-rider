from PyQt6.QtWidgets import QApplication

from app.widgets.focus_border_widget import FocusBorderWidget


class OverlayController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.focus_borders = []
        self._create_focus_borders()

        self.app.data.app_events.timer_started.connect(self.display_overlay)
        self.app.data.app_events.timer_paused.connect(self.hide_overlay)

        qapp = QApplication.instance()
        if qapp:
            qapp.screenAdded.connect(self._handle_screen_added)
            qapp.screenRemoved.connect(self._handle_screen_removed)

    def _create_focus_borders(self):
        for border in self.focus_borders:
            border.hide()
            border.deleteLater()
        self.focus_borders.clear()

        screens = QApplication.screens()
        for screen in screens:
            border = FocusBorderWidget(
                on_close_callback=self.on_focus_border_closed, target_screen=screen
            )
            border.hide()
            self.focus_borders.append(border)

    def _handle_screen_added(self, screen):
        border = FocusBorderWidget(
            on_close_callback=self.on_focus_border_closed, target_screen=screen
        )
        border.hide()
        self.focus_borders.append(border)

    def _handle_screen_removed(self, screen):
        borders_to_remove = [
            b for b in self.focus_borders if b._target_screen == screen
        ]
        for border in borders_to_remove:
            border.hide()
            border.deleteLater()
            self.focus_borders.remove(border)

    def resize(self, event_size):
        pass

    def display_overlay(self):
        top_task = self.app.data.get_top_task()
        if not top_task:
            for border in self.focus_borders:
                border.hide()
            return
        for border in self.focus_borders:
            border.set_task_name(top_task.task_title)
            border.show()
        self.parent.hide()

    def hide_overlay(self):
        for border in self.focus_borders:
            border.hide()
        self.parent.show()

    def on_focus_border_closed(self):
        if (
            hasattr(self.parent, "manage_timer_controller")
            and self.parent.manage_timer_controller.timer_on
        ):
            self.parent.manage_timer_controller.toggle_timer()
