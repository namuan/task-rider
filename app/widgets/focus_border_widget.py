from PyQt6.QtCore import Qt, QRect
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
        self.task_name = ""
        self.on_close_callback = on_close_callback

        self._setup_header()

        screen = QApplication.primaryScreen()
        if screen:
            self.setGeometry(screen.geometry())

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
        self.task_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 8px;
            padding: 8px 16px;
        """)
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
            y = self.border_width + 5
            self.header_widget.move(x, y)

    def showEvent(self, event):
        super().showEvent(event)
        self._position_header()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        border_rect = QRect(
            rect.x() + self.border_width // 2,
            rect.y() + self.border_width // 2,
            rect.width() - self.border_width,
            rect.height() - self.border_width,
        )

        pen = QPen(self.border_color)
        pen.setWidth(self.border_width)
        painter.setPen(pen)
        painter.drawRect(border_rect)

        painter.end()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_header()
