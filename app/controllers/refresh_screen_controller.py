class RefreshScreenController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # app events
        self.app.data.app_events.timer_started.connect(self.resize)
        self.app.data.app_events.timer_paused.connect(self.resize)
        self.app.data.app_events.timer_reset.connect(self.resize)

    def resize(self):
        self.parent.updateScreen()
