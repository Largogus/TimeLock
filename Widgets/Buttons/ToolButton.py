from PySide6.QtWidgets import QToolButton
from PySide6.QtGui import QPainter, QIcon, QColor
from PySide6.QtCore import QSize, Qt


class ToolButton(QToolButton):
    def __init__(self, icon_path=None, icon_size=16, bg_color=None, hover_color=None, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.icon_size_val = icon_size
        self.bg_color = bg_color or Qt.GlobalColor.transparent
        self.hover_color = hover_color or Qt.GlobalColor.gray
        self.hovered = False
        if icon_path:
            self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(icon_size, icon_size))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setAutoRaise(True)
        self.setFixedSize(icon_size + 8, icon_size + 8)

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = self.hover_color if self.hovered else self.bg_color
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 4, 4)

        if self.icon_path:
            icon = QIcon(self.icon_path)
            pixmap = icon.pixmap(self.icon_size_val, self.icon_size_val)
            x = (self.width() - self.icon_size_val) // 2
            y = (self.height() - self.icon_size_val) // 2
            painter.drawPixmap(x, y, pixmap)