from PySide6.QtWidgets import QTextEdit, QFrame, QMenu
from PySide6.QtGui import QColor, QPainter, QBrush, Qt, QFont, QAction


class TextEdit(QTextEdit):
    def __init__(self, border: int = 16, max_char: int = 300, place: str = ""):
        super().__init__()

        self._border = border
        self._background = QColor('#B6B6B6')

        self.max_char = max_char

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        font = QFont("Arial", (self.height() // 2) - 1)
        self.setFont(font)

        self.setPlaceholderText(place)

        self.textChanged.connect(self.check_len)

    def setMaximum(self, size: int):
        self.setMaximumHeight(size)

        font = QFont("Arial", (self.height() // 2))
        self.setFont(font)

        self.update()

    def check_len(self):
        text = self.toPlainText()

        if len(text) > self.max_char:
            self.setPlainText(text[:self.max_char])
            cursor = self.textCursor()
            pos = cursor.position()
            self.blockSignals(True)
            self.setPlainText(text[:self.max_char])
            cursor.setPosition(max(pos, self.max_char))
            self.setTextCursor(cursor)
            self.blockSignals(False)

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        painter.setBrush((QBrush(self._background)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, self._border, self._border)

        super().paintEvent(event)

    def setText(self, text):
        super().setText(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        undo_action = QAction("Отменить", self)
        undo_action.triggered.connect(self.undo)
        menu.addAction(undo_action)

        redo_action = QAction("Повторить", self)
        redo_action.triggered.connect(self.redo)
        menu.addAction(redo_action)

        menu.addSeparator()

        cut_action = QAction("Вырезать", self)
        cut_action.triggered.connect(self.cut)
        menu.addAction(cut_action)

        copy_action = QAction("Копировать", self)
        copy_action.triggered.connect(self.copy)
        menu.addAction(copy_action)

        paste_action = QAction("Вставить", self)
        paste_action.triggered.connect(self.paste)
        menu.addAction(paste_action)

        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.textCursor().removeSelectedText)
        menu.addAction(delete_action)

        menu.addSeparator()

        select_all_action = QAction("Выделить всё", self)
        select_all_action.triggered.connect(self.selectAll)
        menu.addAction(select_all_action)

        menu.exec(event.globalPos())