from PySide6.QtWidgets import QWidget, QSizePolicy
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect
from Widgets.Buttons.Button import Button


class PanelTemplate(QWidget):
    def __init__(self, parent=None, width: int = 400, background_color: QColor = QColor("#13261D"), alpha: int = 225):
        super().__init__(parent)

        self._width = width
        self._bg = background_color
        self._alpha = alpha
        self._is_hide = True

        self.setGeometry(0, 0, 0, 0)

        self.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )

        self.close_btn = Button(
            "X",
            font_size=20,
            font_color=Qt.GlobalColor.white,
            radius=0,
            alpha=[0, 0, 0],
            margin=6,
            align=Qt.AlignmentFlag.AlignCenter
        )

        self.close_btn.setFixedSize(20, 20)
        self.close_btn.clicked.connect(self.closePanel)

        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        bg = QColor(self._bg)
        bg.setAlpha(self._alpha)

        painter.setBrush(bg)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        super().paintEvent(event)

    def toggle(self):
        if not self.parent():
            return

        self.animation.stop()
        parent_width = self.parent().width()
        parent_height = self.parent().height()

        if self._is_hide:
            start_rect = QRect(parent_width, 0, 0, parent_height)
            end_rect = QRect(parent_width - self._width, 0, self._width, parent_height)
        else:
            start_rect = QRect(parent_width - self._width, 0, self._width, parent_height)
            end_rect = QRect(parent_width, 0, 0, parent_height)

        self.raise_()

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()

        self._is_hide = not self._is_hide

    def closePanel(self):
        self.toggle()

    def upd(self):
        if not self._is_hide:
            parent_width = self.parent().width()
            parent_height = self.parent().height()
            self.setGeometry(parent_width - self._width, 0, self._width, parent_height)

    def reopen(self, date, func):
        if self._is_hide:
            func(date)
        self.toggle()