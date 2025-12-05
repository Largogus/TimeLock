from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPainter, QBrush, QColor, QPen


class Button(QPushButton):
    def __init__(self, name: str, font_size: int = 14, min: int = 165, max: int = 500):
        super().__init__()

        self.RADIUS = 15
        self.BG_COLOR = QColor('#B6B6B6')
        self.PRESSER_COLOR = QColor('#969696')
        self.HOVERED_COLOR = QColor('#ADADAD')

        self.BORDER_WIDTH = 1

        self.setMinimumHeight(40)
        self.setMinimumWidth(min)

        self.setMaximumWidth(max)

        self.name = name
        self.hovered = False
        self.FONT_SIZE = font_size

        self.setMouseTracking(True)

    def paintEvent(self, event):
        paint = QPainter(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        if self.isDown():
            color = self.PRESSER_COLOR
        elif self.hovered:
            color = self.HOVERED_COLOR
        else:
            color = self.BG_COLOR

        paint.setBrush((QBrush(color)))
        paint.setPen(Qt.PenStyle.NoPen)
        paint.drawRoundedRect(rect, self.RADIUS, self.RADIUS)

        font = paint.font()
        font.setPixelSize(self.FONT_SIZE)
        paint.setFont(font)

        paint.setPen(Qt.GlobalColor.black)
        paint.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.name)

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)