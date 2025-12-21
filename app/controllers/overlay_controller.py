from app.widgets.overlay_widget import Overlay


class OverlayController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        self.overlay = Overlay(self.parent.lst_tasks)
        self.overlay.hide()

        # app events
        self.app.data.app_events.timer_started.connect(self.display_overlay)
        self.app.data.app_events.timer_paused.connect(self.hide_overlay)

    def resize(self, event_size):
        self.overlay.resize(event_size)

    def display_overlay(self):
        top_task = self.app.data.get_top_task()
        if not top_task:
            self.overlay.hide()
            return
        self.overlay.setTitle(top_task.task_title)
        self.overlay.show()

    def hide_overlay(self):
        self.overlay.hide()
