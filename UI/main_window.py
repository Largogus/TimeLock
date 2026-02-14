from PySide6.QtGui import QColor, QIcon, QPixmap
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, QSpacerItem
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from UI.screen.applications import Applications
from core.system.desktop import DesktopSize
from Widgets.Button import Button
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from UI.screen.home import Home


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1300, 600)
        self.setMinimumSize(1300, 600)
        self.setWindowTitle('TimeLock')
        self.setWindowIcon(QIcon('src/icon.png'))

        # self.signal = SignalObject()
        # self.signal.change_window.connect(self.change_window)

        x, y = DesktopSize(self)

        self.move(x, y)

        '''------------------'''

        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.sidebar = BaseFrame(border=0, box=QVBoxLayout())
        self.sidebar.setContentsMargins(0, 0, 0, 0)
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.sidebar.setFixedWidth(200)
        self.sidebar.setMinimumWidth(55)

        self.stacked = QStackedWidget()
        self.stacked.setMinimumSize(300, 100)
        self.stacked.setContentsMargins(0, 0, 0, 0)

        sidebar_buttons = []

        self.header = BaseFrame(border=0)

        self.header.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.header.mainLayout.setSpacing(0)

        self.logo = QLabel()
        img = QPixmap("src/image/TimeLock.png")
        self.logo.setPixmap(img)
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(64, 50)

        self.cur_img_header = "src/icon/left_panel_close.svg"
        self.button = Button("", min=33, svg_path=self.cur_img_header, ratio=28, scale=2, alpha=[0, 0, 0])
        self.button.clicked.connect(self.toggle_sideboard)

        space = QSpacerItem(150, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.header.addElement(self.logo)
        self.header.addSpacer(space)
        self.header.addElement(self.button, alignment=Qt.AlignmentFlag.AlignRight)

        self.sidebar.addElement(self.header)
        self.sidebar.addElement(Line())

        self.main = BaseFrame(border=0, box=QVBoxLayout())
        self.main.mainLayout.setContentsMargins(0, 0, 0, 0)

        button_home = Button("Обзор", min=64, svg_path="src/icon/home.svg", ratio=28, scale=2, font_size=20,
                             radius=20, alpha=[0, 50, 100])
        button_home.setBackgroundHover()
        button_home.clicked.connect(lambda: print(42))
        sidebar_buttons.append(button_home)

        button_application = Button("Приложения", min=64, svg_path="src/icon/computer.svg", ratio=28, scale=2,
                                    font_size=20, alpha=[0, 50, 100], radius=20)
        button_application.clicked.connect(lambda: print(42))
        sidebar_buttons.append(button_application)

        button_limit = Button("Лимиты", min=64, svg_path="src/icon/hourglass.svg", ratio=28, scale=2, font_size=20,
                              alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_limit)

        button_focus = Button("Фокус", min=64, svg_path="src/icon/focus.svg", ratio=28, scale=2, font_size=20,
                              alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_focus)

        button_stat = Button("Статистика", min=64, svg_path="src/icon/statistic.svg", ratio=28, scale=2, font_size=20,
                             alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_stat)

        button_history = Button("История", min=64, svg_path="src/icon/history.svg", ratio=28, scale=2, font_size=20,
                                alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_history)

        button_settings = Button("Настройки", min=64, svg_path="src/icon/settings.svg", ratio=28, scale=2,
                                 font_size=20, alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_settings)

        for btn in sidebar_buttons:
            btn.setBackgroundHover(QColor('#24c72a'))
            btn.setBackgroundPressed(QColor('#24c72a'))
            text = btn.getText()
            btn.clicked.connect(lambda _, t=text: self.change_window(t))
            self.main.addElement(btn)

        self.sidebar.addElement(self.main)

        self.stacked.addWidget(Home())
        self.stacked.addWidget(Applications())
        self.sidebar.mainLayout.addStretch(1)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stacked)

        self.is_small = False
        self.window_small = False

        self.setCentralWidget(central_widget)

    def toggle_sideboard(self):
        if not self.window_small:
            start_width = self.sidebar.width()
            end_width = 55 if not self.is_small else 200

            if self.cur_img_header == "src/icon/left_panel_open.svg":
                self.button.setImage("src/icon/left_panel_close.svg")
                self.cur_img_header = "src/icon/left_panel_close.svg"
            else:
                self.button.setImage("src/icon/left_panel_open.svg")
                self.cur_img_header = "src/icon/left_panel_open.svg"

            animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
            animation.setDuration(300)
            animation.setStartValue(start_width)
            animation.setEndValue(end_width)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation.start()

            self.is_small = not self.is_small
            self.animation = animation

            if self.logo.isHidden():
                self.logo.show()
            else:
                self.logo.hide()

    def change_window(self, data: str):
        if data == "Обзор":
            self.stacked.setCurrentIndex(0)
        elif data == "Приложения":
            self.stacked.setCurrentIndex(1)

    def resizeEvent(self, event):
        width = self.width()
        print(width, self.height())

        if width < 856:
            if not self.is_small:
                self.toggle_sideboard()

            self.window_small = True

        if width > 856:
            self.window_small = False

            if self.window_small:
                self.logo.show()