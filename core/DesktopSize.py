from PySide6.QtGui import QGuiApplication


def DesktopSize(screen):
    SCREEN = screen.geometry()
    DESKTOP = QGuiApplication.primaryScreen().geometry()

    x = (DESKTOP.width() - SCREEN.width()) // 2
    y = (DESKTOP.height() - SCREEN.height()) // 2

    return (x, y)