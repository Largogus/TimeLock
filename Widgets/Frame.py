from PySide6.QtWidgets import QFrame, QHBoxLayout, QLayout
from PySide6.QtGui import QPainter, QColor, QBrush, Qt, QFont
from typing import Optional
from core.system.config import FONT_FAMILY


class BaseFrame(QFrame):
    def __init__(self, box: Optional[QLayout] = None, border: int = 10, text: str = None):
        super().__init__()

        self._bg = QColor('#CFCFCF')
        self._border = border
        self._text = text
        self._font_size = 12
        self._font_family = FONT_FAMILY

        self.mainLayout = box or QHBoxLayout()

        self.setLayout(self.mainLayout)

    def setBorderRadius(self, border_radius: int):
        self._border = border_radius
        self.update()

    def setBackgroundColor(self, bg: QColor = QColor('#CFCFCF'), alpha: int = None):
        color = QColor(bg)

        if alpha is not None:
            color.setAlpha(alpha)

        self._bg = color
        self.update()

    def setFontFrame(self, family: str = FONT_FAMILY, size: int = 12):
        self._font_family = family
        self._font_size = size
        self.update()

    def addElement(self, elm, alignment: Optional[Qt.AlignmentFlag] = None):
        if alignment is not None:
            self.mainLayout.addWidget(elm, alignment=alignment)
        else:
            self.mainLayout.addWidget(elm)

    def addLayout(self, elm):
            self.mainLayout.addLayout(elm)

    def addSpacer(self, elm):
            self.mainLayout.addSpacerItem(elm)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        painter.setBrush((QBrush(self._bg)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

        if self._text is not None:
            painter_font = painter.font()
            painter_font.setPixelSize(self._font_size)
            painter_font.setWeight(QFont.Weight.Bold)
            painter_font.setFamily(self._font_family)
            painter.setFont(painter_font)
            painter.setPen(Qt.GlobalColor.black)

            painter.drawText(rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text)

        super().paintEvent(event)