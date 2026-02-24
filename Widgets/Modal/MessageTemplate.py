from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QIcon, QFont, QPalette, QColor
from PySide6.QtCore import Qt
from core.system.config import FONT_FAMILY, ICON_PATH


def MessageTemplate(msg_icon: QMessageBox.Icon, text, title="Кнопка заблокирована", icon: QIcon = QIcon(ICON_PATH),
                    standard_btn: QMessageBox.StandardButton = QMessageBox.StandardButton.Ok):
    msg = QMessageBox()

    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(msg_icon)

    font = QFont(FONT_FAMILY, 12, QFont.Weight.Bold)
    msg.setFont(font)

    msg.setWindowIcon(icon)

    msg.setWindowFlags(msg.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)

    msg.setStandardButtons(standard_btn)
    ok_btn = msg.button(standard_btn)
    ok_btn.setAutoFillBackground(False)

    msg.exec()