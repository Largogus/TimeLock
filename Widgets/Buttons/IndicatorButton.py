from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, Property
from PySide6.QtGui import QPainter, QBrush, QColor, QFont

from Widgets.Buttons.Button import Button
from Widgets.Modal.DisabledMessageModal import show_disabled_message


class IndicatorButton(Button):
    def __init__(self, *args, state: bool = False, indicator_color: QColor = QColor("#5bff3b"), radius: int = 15, margin: int = 6, **kwargs):
        super().__init__(*args, **kwargs)

        self.RADIUS = radius
        self.MARGIN = margin
        self.STATE = state

        self.TRUE_COLOR = QColor("#c41000")
        self.FALSE_COLOR = QColor("#5bff3b")

        self._current_color = self.TRUE_COLOR if self.STATE else self.FALSE_COLOR

        self.indicator_anim = QPropertyAnimation(self, b"indicatorColor")
        self.indicator_anim.setDuration(400)
        self.INDICATOR_OFFSET = self.RADIUS * 2 + self.MARGIN

        self.setContentsMargins(self.RADIUS*2 + self.MARGIN*2, 0, 0, 0)

    def paintEvent(self, event):
        super().paintEvent(event)

        paint = QPainter(self)
        paint.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        x = self.MARGIN + 6
        y = rect.center().y() - (self.RADIUS - 1)

        paint.setBrush(self._current_color)
        paint.setPen(Qt.PenStyle.NoPen)
        paint.drawEllipse(x, y, self.RADIUS * 2, self.RADIUS * 2)

    def getIndicatorColor(self):
        return self._current_color

    def setIndicatorColor(self, color: QColor):
        self._current_color = color
        self.update()

    def mousePressButton(self):
        self.indicator_anim.stop()

        self.STATE = not self.STATE

        if not self.STATE:
            self.indicator_anim.setStartValue(self.TRUE_COLOR)
            self.indicator_anim.setEndValue(self.FALSE_COLOR)
        else:
            self.indicator_anim.setStartValue(self.FALSE_COLOR)
            self.indicator_anim.setEndValue(self.TRUE_COLOR)

        self.indicator_anim.start()

    indicatorColor = Property(QColor, getIndicatorColor, setIndicatorColor)