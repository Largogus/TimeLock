from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QBrush, QFont
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from core.system.config import FONT_FAMILY


class CategoryCard(QPushButton):
    def __init__(self, title, time):
        super().__init__()

        self._bg = QColor('#A7E6BE')
        self._bg_hover = QColor('#24c72a')
        self._border = 16
        self._font_size = 20
        self._hover = False

        self._title = title
        self._time = time

        self.setFixedSize(240, 120)

        self.mainLayout = QHBoxLayout()

        self.setLayout(self.mainLayout)

        self.setMouseTracking(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        if self._hover:
            bg = self._bg_hover
            bg.setAlpha(100)
        else:
            bg = self._bg
            bg.setAlpha(200)

        painter.setBrush((QBrush(bg)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

        title_font = painter.font()
        title_font.setPixelSize(self._font_size)
        title_font.setWeight(QFont.Weight.Bold)

        painter.setFont(title_font)
        painter.setPen(QColor('#1F2D2A'))

        rect_title = QRectF(rect)
        rect_title.setTop(rect.top() - 70)

        rect_time = QRectF(rect)
        rect_time.setTop(rect.top() + 25)

        painter.drawText(rect_title, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter, self._title)

        painter.setPen(QColor('#3A4A46'))
        painter.drawText(rect_time, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter, self._time)

    def leaveEvent(self, event):
        self._hover = False
        self.update()

        super().leaveEvent(event)

    def enterEvent(self, event):
        self._hover = True
        self.update()

        super().enterEvent(event)