from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog
from PySide6.QtGui import QFont, QPalette, QColor, QKeyEvent
from PySide6.QtCore import Qt
from core.system.config import FONT_FAMILY


class TemplateClose(QDialog):
    def __init__(self, defer: bool):
        super().__init__()

        font = QFont(FONT_FAMILY, 14)
        font.setBold(True)

        self.defer = defer

        self.setFont(font)
        self.setWindowFlags(Qt.WindowType.WindowTitleHint |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.WindowDoesNotAcceptFocus
                            )

        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#fdb4b4"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))

        self.lay = QVBoxLayout()

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.lay)
        self.setPalette(palette)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_F4 and event.modifiers() & Qt.KeyboardModifier.AltModifier:
            event.ignore()
        else:
            super().keyPressEvent(event)