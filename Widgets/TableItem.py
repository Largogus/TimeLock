from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QColor, QPainter, QPen, QBrush, Qt


class TableItem(QWidget):
    def __init__(self, parent=None, title: str = "", path: str = "/"):
        super().__init__()

        self.BACKGROUND_COLOR = QColor('#AFAFAF')
        self.RADIUS = 15
        self.TITLE = title
        self.PATH = f"Путь: {path}"
        self.setMinimumSize(300, 50)

        self.parent = parent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(QBrush(self.BACKGROUND_COLOR))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), self.RADIUS, self.RADIUS)\

        font = painter.font()
        font.setPixelSize(14)

        painter.setPen(Qt.GlobalColor.black)

        x = 20
        new_x = (14 * len(self.TITLE)) + 20

        painter.drawText(x, 29, self.TITLE)

        painter.setPen(QColor(0, 0, 0, 100))
        painter.drawText(new_x, 29, self.PATH)

        painter.setFont(font)

    def mousePressEvent(self, btn):
        if btn.button() == Qt.MouseButton.LeftButton:
            print("Кнопка работает")