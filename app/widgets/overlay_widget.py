from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QPainter, QBrush, QColor, QFont
from PyQt5.QtWidgets import QWidget, QApplication


class Overlay(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.task_title = None

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.parent.rect(), QBrush(QColor(127, 127, 127)))

        if self.task_title:
            font: QFont = QApplication.font()
            font.setPointSize(40)
            painter.setFont(font)
            painter.setPen(Qt.white)
            painter.drawText(
                self.parent.rect(), Qt.AlignLeft | Qt.AlignTop | Qt.TextWordWrap, self.task_title
            )
        painter.end()

    def setTitle(self, title):
        self.task_title = title
