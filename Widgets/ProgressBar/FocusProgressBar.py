from PySide6.QtCore import Qt, QRectF, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtWidgets import QWidget

from core.system.date import normal_time, to_time, plural


class FocusProgressBar(QWidget):
    def __init__(self, total_time):
        super().__init__()

        self.total_time = total_time
        self.remaining_time = 0

        self.setMinimumSize(100, 100)

    def updateRemainingTime(self, remaining):
        self.remaining_time = max(0, min(remaining, self.total_time))
        self.update()

    def setTotalTime(self, value):
        self.total_time = value
        self.update()

    def progressColor(self):
        if self.total_time == 0:
            return QColor("#909fb6")

        percent = (self.total_time - self.remaining_time) / self.total_time

        return QColor("#4CAF50")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = min(self.width(), self.height())
        margin = size * 0.08
        pen_width = int(size * 0.08)

        rect = QRectF(
            margin,
            margin,
            size - 2 * margin,
            size - 2 * margin
        )

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#c6d6d3"))
        painter.drawEllipse(rect)

        if self.total_time > 0:
            percent = self.remaining_time / self.total_time
            angle = percent * 360
        else:
            angle = 0

        progress_pen = QPen(self.progressColor())
        progress_pen.setWidth(pen_width)
        progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(progress_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawArc(rect, 90 * 16, -angle * 16)

    def sizeHint(self):
        return QSize(260, 260)