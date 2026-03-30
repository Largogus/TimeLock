from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPalette, QColor, QPainter, QBrush, QPen
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QHBoxLayout
from Widgets.Buttons.Button import Button


class Notification(QWidget):
    closed = Signal()

    def __init__(self, message: str, duration=3000, parent=None):
        super().__init__(parent)

        self.message = message
        self.duration = duration

        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint |
                            Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.WindowDoesNotAcceptFocus |
                            Qt.WindowType.Tool)

        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowOpacity(0.95)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.Text, QColor("white"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        self.label = QLabel()

        self.label.setPalette(palette)

        L_F = self.label.font()
        L_F.setBold(True)
        L_F.setPointSize(16)

        self.label.setFont(L_F)

        close_btn = Button(
            "X",
            font_size=20,
            font_color=Qt.GlobalColor.white,
            radius=0,
            alpha=[10, 10, 10],
            margin=6,
            align=Qt.AlignmentFlag.AlignCenter
        )

        title_app = QLabel()
        title_app.setText("TimeLock")

        T_F = title_app.font()
        T_F.setPointSize(18)
        T_F.setBold(True)

        title_app.setFont(T_F)

        close_btn.setFixedSize(20, 20)
        close_btn.clicked.connect(self.close)

        h_lay = QHBoxLayout()
        v_lay = QVBoxLayout()

        h_lay.addWidget(title_app, alignment=Qt.AlignmentFlag.AlignLeft)
        h_lay.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignRight)
        v_lay.addWidget(self.label)

        layout.addLayout(h_lay)
        layout.addLayout(v_lay)
        layout.setContentsMargins(15, 10, 15, 10)

    def show_notification(self, name, hwnd):
        screen = QApplication.primaryScreen()
        geom = screen.availableGeometry()

        text = self.message.replace("%app%", name or "")
        self.label.setText(text)
        self.adjustSize()

        w, h = self.width(), self.height()
        x = geom.right() - w - 20
        y = geom.bottom() - h - 20

        self.setGeometry(int(x), int(y), int(w), int(h))
        self.show()
        self.raise_()

        QTimer.singleShot(self.duration, self.close)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        painter.setBrush(QBrush(QColor(50, 50, 50)))

        pen = QPen(QColor("white"))
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(rect.adjusted(0, 0, -1, -1), 12, 12)