from PySide6.QtWidgets import QFrame, QHBoxLayout, QLayout
from PySide6.QtGui import QPainter, QColor, QBrush, Qt
from typing import Optional


class BaseFrame(QFrame):
    def __init__(self, box: Optional[QLayout] = None):
        super().__init__()

        self._bg = QColor('#CFCFCF')
        self._border = 10

        self.mainLayout = box or QHBoxLayout()

        self.setLayout(self.mainLayout)

    def setBorderRadius(self, border_radius: int):
        self._border = border_radius
        self.update()

    def setBackgroundColor(self, bg: QColor):
        self._bg = bg
        self.update()

    def addElement(self, elm):
        self.mainLayout.addWidget(elm)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        painter.setBrush((QBrush(self._bg)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

        super().paintEvent(event)