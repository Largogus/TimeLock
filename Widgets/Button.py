from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QBrush, QColor, QPen


class Button(QPushButton):
    def __init__(self, name: str):
        super().__init__()

        self.RADIUS = 15
        self.BG_COLOR = QColor('#B6B6B6')
        self.PRESSER_COLOR = QColor('#969696')

        self.BORDER_WIDTH = 1

        self.setMinimumHeight(40)
        self.setMinimumWidth(150)

        self.name = name

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        color = self.PRESSER_COLOR if self.isDown() else self.BG_COLOR

        paint.setBrush((QBrush(color)))
        paint.setPen(Qt.PenStyle.NoPen)
        paint.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

        paint.setPen(Qt.GlobalColor.black)
        paint.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)


