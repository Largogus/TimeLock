from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLineEdit, QFrame, QMenu
from PySide6.QtCore import QSize, QRectF
from PySide6.QtGui import QColor, QPainter, QBrush, Qt, QFont, QAction, QPen


class TextEdit(QLineEdit):
    def __init__(
        self,
        placeholder: str = "",
        max_char: int = 300,
        border_radius: int = 16,
        background: QColor = QColor("#AFAFAF"),
        alpha: int = 255,
        image: str = None,
        ratio: float = 0.45
    ):

        super().__init__()

        self._bg = background
        self._alpha = alpha
        self._border = border_radius
        self._error = False
        self._ratio = ratio

        self._font_size = 16

        font = self.font()
        font.setPointSize(self._font_size)
        self.setFont(font)

        self.renderer = QSvgRenderer(image) if image else None

        self.setFrame(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPlaceholderText(placeholder)
        self.setMaxLength(max_char)

        self.setStyleSheet('background-color: transparent')

        self.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        h = self.height()
        if h > 10:
            font = self.font()
            font.setPixelSize(int(h * self._ratio))
            font.setBold(True)
            self.setFont(font)
        super().resizeEvent(event)

    def setError(self, value: bool):
        self._error = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        bg = QColor(self._bg)
        bg.setAlpha(self._alpha)

        painter.setBrush(QBrush(bg))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

        icon_size = 24
        margin = 8

        self.setTextMargins(icon_size + 2*margin, 0, margin, 0)

        rect_image = QRectF(
            margin, (self.height() - icon_size) // 2, icon_size, icon_size
        )

        self.renderer.render(painter, rect_image)

        if self._error:
            rect.adjust(2, 2, -2, -2)
            painter.setPen(QPen(QColor("red"), 2))
            painter.drawRoundedRect(rect, self._border, self._border)

        super().paintEvent(event)

    def sizeHint(self) -> QSize:
        return QSize(300, 60)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        actions = [
            ("Отменить", self.undo),
            ("Вырезать", self.cut),
            ("Копировать", self.copy),
            ("Вставить", self.paste),
            ("Удалить", self.clear),
            ("Выделить всё", self.selectAll),
        ]

        for text, slot in actions:
            act = QAction(text, self)
            act.triggered.connect(slot)
            menu.addAction(act)

        menu.exec(event.globalPos())