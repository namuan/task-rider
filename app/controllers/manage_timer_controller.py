from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound


class Timer:
    def __init__(self, timer_value, callback):
        self.t = QTimer()
        self.t.timeout.connect(self.fired)
        self.initial_value = timer_value
        self.timer_value = timer_value
        self.callback = callback

    def get_time(self):
        return self.timer_value

    def start(self):
        self.t.start(1000)

    def pause(self):
        self.t.stop()

    def reset(self):
        self.pause()
        self.timer_value = self.initial_value
        self.callback(self.timer_value)

    def fired(self):
        self.timer_value = self.timer_value - 1
        self.callback(self.timer_value)


class BellSound:
    def __init__(self):
        self.sound = QSound(":/sounds/bell.wav")

    def ring(self):
        self.sound.play()


class ManageTimerController:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.timer_on = False
        self.initial_timer_value = int(self.parent.lbl_timer_value.text())
        self.timer = Timer(timer_value=self.initial_timer_value * 60, callback=self.on_timer_fired)
        self.bell = BellSound()

        # ui events
        self.parent.btn_toggle_timer.pressed.connect(self.toggle_timer)
        self.parent.btn_reset_timer.pressed.connect(self.reset_timer)

    def on_timer_fired(self, current_value):
        self.parent.lbl_timer_value.setText(self.convert_to_minutes(current_value))
        if current_value <= 0:
            self.bell.ring()
            self.timer.reset()
            self.toggle_timer()

    def toggle_timer(self):
        self.timer_on = not self.timer_on
        self.update_button_text()
        if self.timer_on:
            self.timer.start()
        else:
            self.timer.pause()

    def reset_timer(self):
        self.timer.reset()

    def update_button_text(self):
        if self.timer_on:
            self.parent.btn_toggle_timer.setText("Pause")
        else:
            self.parent.btn_toggle_timer.setText("Start")

    def convert_to_minutes(self, seconds):
        return "{}:{:02.0f}".format(int(seconds / 60), seconds % 60)
