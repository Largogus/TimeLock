from PySide6.QtWidgets import QLineEdit, QFrame, QMenu
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QPainter, QBrush, Qt, QFont, QAction, QPen


class TextEdit(QLineEdit):
    def __init__(
        self,
        placeholder: str = "",
        max_char: int = 300,
        border_radius: int = 16,
        background: QColor = QColor("#AFAFAF"),
    ):

        super().__init__()

        self._bg = background
        self._border = border_radius
        self._error = False

        self.setFrame(False)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setPlaceholderText(placeholder)
        self.setMaxLength(max_char)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("QLineEdit { background: transparent; }")

        self.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        h = self.height()
        if h > 10:
            self.setFont(QFont("Arial", int(h * 0.45)))
        super().resizeEvent(event)

    def setError(self, value: bool):
        self._error = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        painter.setBrush(QBrush(self._bg))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

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