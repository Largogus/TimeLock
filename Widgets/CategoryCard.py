from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QBrush, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout


class CategoryCard(QFrame):
    def __init__(self):
        super().__init__()

        self._bg = QColor('#13261D')
        self._bg_hover = QColor('#1E3D2B')
        self._border = 16
        self._font_size = 12
        self._font_family = 'Segoe UI'
        self._hover = False

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
        else:
            bg = self._bg

        painter.setBrush((QBrush(bg)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

        # if self._text is not None:
        #     painter_font = painter.font()
        #     painter_font.setPixelSize(self._font_size)
        #     painter_font.setWeight(QFont.Weight.Bold)
        #     painter_font.setFamily(self._font_family)
        #     painter.setFont(painter_font)
        #     painter.setPen(Qt.GlobalColor.black)
        #
        #     painter.drawText(rect, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._text)

        super().paintEvent(event)

    def leaveEvent(self, event):
        self._hover = False
        self.update()

        super().leaveEvent(event)

    def enterEvent(self, event):
        self._hover = True
        self.update()

        super().enterEvent(event)