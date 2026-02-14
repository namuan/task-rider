import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont
from PyQt6.QtWidgets import QWidget, QPushButton, QApplication, QHBoxLayout, QLabel


class FocusBorderWidget(QWidget):
    def __init__(self, on_close_callback=None):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        self.border_color = QColor(0, 122, 255)
        self.border_width = 8
        self.top_border_width = 45
        self.task_name = ""
        self.on_close_callback = on_close_callback
        self._macos_properties_set = False

        self._setup_header()

        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.geometry())

    def _setup_macos_window_properties(self):
        if self._macos_properties_set:
            return
        if sys.platform != "darwin":
            return

        try:
            from ctypes import c_void_p, CDLL, c_bool, c_uint

            NSWindowCollectionBehaviorCanJoinAllSpaces = 1 << 0
            NSWindowCollectionBehaviorFullScreenAuxiliary = 1 << 8

            view_id = int(self.winId())

            objc = CDLL(None)
            objc.objc_getClass.restype = c_void_p
            objc.sel_registerName.restype = c_void_p

            send_msg = objc.objc_msgSend
            send_msg.restype = c_void_p
            send_msg.argtypes = [c_void_p, c_void_p]

            window_sel = objc.sel_registerName(b"window")
            window = send_msg(view_id, window_sel)

            if window:
                self._macos_properties_set = True

                set_hides_sel = objc.sel_registerName(b"setHidesOnDeactivate:")
                send_msg.argtypes = [c_void_p, c_void_p, c_bool]
                send_msg(window, set_hides_sel, False)

                collection_behavior = (
                    NSWindowCollectionBehaviorCanJoinAllSpaces
                    | NSWindowCollectionBehaviorFullScreenAuxiliary
                )
                set_cb_sel = objc.sel_registerName(b"setCollectionBehavior:")
                send_msg.argtypes = [c_void_p, c_void_p, c_uint]
                send_msg(window, set_cb_sel, collection_behavior)
        except Exception:
            pass

    def _setup_header(self):
        self.header_widget = QWidget(self)
        self.header_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QHBoxLayout(self.header_widget)
        layout.setContentsMargins(20, 10, 20, 10)

        layout.addStretch()

        self.task_label = QLabel(self.header_widget)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.task_label.setFont(font)
        self.task_label.setStyleSheet(
            """
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 8px;
            padding: 8px 16px;
        """
        )
        layout.addWidget(self.task_label)

        self.close_button = QPushButton("✕", self.header_widget)
        self.close_button.setFixedSize(30, 30)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setStyleSheet(
            """
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 0.7);
            }
        """
        )
        self.close_button.clicked.connect(self._on_close_clicked)
        layout.addWidget(self.close_button)

        layout.addStretch()

        self.header_widget.adjustSize()

    def _on_close_clicked(self):
        self.hide()
        if self.on_close_callback:
            self.on_close_callback()

    def set_task_name(self, name):
        self.task_name = name if name else ""
        self.task_label.setText(self.task_name)
        self.header_widget.adjustSize()
        self._position_header()

    def _position_header(self):
        screen = QApplication.primaryScreen()
        if screen:
            screen_geometry = screen.geometry()
            header_width = self.header_widget.sizeHint().width()
            x = (screen_geometry.width() - header_width) // 2
            y = self.top_border_width + 5
            self.header_widget.move(x, y)

    def showEvent(self, event):
        super().showEvent(event)
        self._setup_macos_window_properties()
        self._position_header()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        QPen(self.border_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.border_color)

        painter.drawRect(rect.x(), rect.y(), rect.width(), self.top_border_width)
        painter.drawRect(rect.x(), rect.y(), self.border_width, rect.height())
        painter.drawRect(
            rect.x(),
            rect.y() + rect.height() - self.border_width,
            rect.width(),
            self.border_width,
        )
        painter.drawRect(
            rect.x() + rect.width() - self.border_width,
            rect.y(),
            self.border_width,
            rect.height(),
        )

        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_header()
