class ManageTimerController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.timer_on = False

        # ui events
        self.parent.btn_toggle_timer.pressed.connect(self.toggle_timer)

    def toggle_timer(self):
        self.timer_on = not self.timer_on
        self.update_button_text()

    def update_button_text(self):
        if self.timer_on:
            self.parent.btn_toggle_timer.setText("Pause")
        else:
            self.parent.btn_toggle_timer.setText("Start")
