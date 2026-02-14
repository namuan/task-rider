from app.widgets.focus_border_widget import FocusBorderWidget


class OverlayController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.focus_border = FocusBorderWidget(
            on_close_callback=self.on_focus_border_closed
        )
        self.focus_border.hide()

        self.app.data.app_events.timer_started.connect(self.display_overlay)
        self.app.data.app_events.timer_paused.connect(self.hide_overlay)

    def resize(self, event_size):
        pass

    def display_overlay(self):
        top_task = self.app.data.get_top_task()
        if not top_task:
            self.focus_border.hide()
            return
        self.focus_border.set_task_name(top_task.task_title)
        self.focus_border.show()
        self.parent.hide()

    def hide_overlay(self):
        self.focus_border.hide()
        self.parent.show()

    def on_focus_border_closed(self):
        if (
            hasattr(self.parent, "manage_timer_controller")
            and self.parent.manage_timer_controller.timer_on
        ):
            self.parent.manage_timer_controller.toggle_timer()
