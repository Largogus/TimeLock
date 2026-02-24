from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication


def DesktopSize(widget) -> tuple:
    screen = QApplication.primaryScreen().availableGeometry()
    x = (screen.width() - widget.width()) // 2
    y = (screen.height() - widget.height()) // 2

    return (x, y)