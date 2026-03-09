from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QPainter, QBrush, QFont
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QGraphicsDropShadowEffect


class HistoryCard(QPushButton):
    clicked = Signal(str)

    def __init__(self, title, last_session, time, session_count, bg: QColor = QColor('#A7E6BE'), bg_hover: QColor = QColor('#24c72a'), w: int = 400, h: int = 100):
        super().__init__()

        self._bg = bg
        self._bg_hover = bg_hover
        self._border = 16
        self._font_size = 16
        self._hover = False

        self._title = title

        self._last_session = last_session

        self._time = time

        self._session_count = session_count

        self.w, self.h = (w, h)

        self.setFixedSize(self.w, self.h)

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
        rect_title.setLeft(rect.left() + 10)
        rect_title.setTop(rect.top() - (self.h // 2))

        rect_time = QRectF(rect)
        rect_time.setLeft(rect.left() + 10)
        rect_time.setTop(rect.top())

        tas = f"{self._time} • {self._session_count} сессий"

        rect_tes = QRectF(rect)
        rect_tes.setLeft(rect.left() + 10)
        rect_tes.setTop(rect.top() + (self.h // 2))

        painter.drawText(rect_title, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, self._title)

        painter.setPen(QColor('#3A4A46'))
        painter.drawText(rect_time, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, str(self._last_session))

        painter.drawText(rect_tes, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft, tas)

    def leaveEvent(self, event):
        self._hover = False
        self.update()

        super().leaveEvent(event)

    def enterEvent(self, event):
        self._hover = True
        self.update()

        super().enterEvent(event)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

        self.clicked.emit(self._title)