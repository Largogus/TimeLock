from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
from PySide6.QtCore import Qt
from core.system.config import FONT_FAMILY


def show_disabled_message(text, title="Кнопка заблокирована"):
    palette_msg = QPalette()
    palette_msg.setColor(QPalette.ColorRole.WindowText, QColor('black'))
    palette_msg.setColor(QPalette.ColorRole.Window, QColor('white'))

    msg = QMessageBox()

    # msg.setPalette(palette_msg)

    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)

    ok_btn = msg.button(QMessageBox.StandardButton.Ok)
    ok_btn.setAutoFillBackground(False)

    font = QFont(FONT_FAMILY, 12, QFont.Weight.Bold)
    msg.setFont(font)

    msg.setWindowIcon(QIcon(":src/icon/block.svg"))

    msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

    msg.exec()