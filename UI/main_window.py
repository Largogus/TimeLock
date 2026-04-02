from PySide6.QtGui import QColor, QIcon, QPixmap, QAction
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, \
    QSpacerItem, QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from UI.screen.applications import Applications
from UI.screen.focus import Focus
from UI.screen.history import History
from UI.screen.limit import Limit
from UI.screen.settings import Settings
from UI.screen.statistics import Statistics
from core.signals.statistics_signsl import stats_signal
from core.system.desktop import DesktopSize
from Widgets.Buttons.Button import Button
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from UI.screen.home import Home
from core.signals.change_signals import signal_change
from core.dataset import resources_rc


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1300, 600)
        self.setMinimumSize(1300, 600)
        self.setWindowTitle('TimeLock')
        self.setWindowIcon(QIcon(":/src/icon.png"))

        self.tray = QSystemTrayIcon(QIcon(":/src/icon.png"), self)

        menu = QMenu()

        show_action = QAction("Открыть", self)
        quit_action = QAction("Выход", self)

        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.quit)

        menu.addAction(show_action)
        menu.addAction(quit_action)

        self.tray.activated.connect(self.on_tray_click)

        self.tray.setContextMenu(menu)
        self.tray.show()

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
        img = QPixmap(":/src/image/TimeLock.png")
        self.logo.setPixmap(img)
        self.logo.setScaledContents(True)
        self.logo.setFixedSize(64, 50)

        self.cur_img_header = ":src/icon/left_panel_close.svg"
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

        button_home = Button("Обзор", min=64, svg_path=":src/icon/home.svg", ratio=28, scale=2, font_size=20,
                             radius=20, alpha=[0, 50, 100])
        button_home.setBackgroundHover()
        sidebar_buttons.append(button_home)

        button_application = Button("Приложения", min=64, svg_path=":src/icon/computer.svg", ratio=28, scale=2,
                                    font_size=20, alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_application)

        button_limit = Button("Лимиты", min=64, svg_path=":src/icon/hourglass.svg", ratio=28, scale=2, font_size=20,
                              alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_limit)

        button_focus = Button("Фокус", min=64, svg_path=":src/icon/focus.svg", ratio=28, scale=2, font_size=20,
                              alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_focus)

        button_stat = Button("Статистика", min=64, svg_path=":src/icon/statistic.svg", ratio=28, scale=2, font_size=20,
                             alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_stat)

        button_history = Button("История", min=64, svg_path=":src/icon/history.svg", ratio=28, scale=2, font_size=20,
                                alpha=[0, 50, 100], radius=20)
        sidebar_buttons.append(button_history)

        button_settings = Button("Настройки", min=64, svg_path=":src/icon/settings.svg", ratio=28, scale=2,
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
        self.stacked.addWidget(Limit())
        self.stacked.addWidget(Focus())
        self.stacked.addWidget(Statistics())
        self.stacked.addWidget(History())
        self.stacked.addWidget(Settings())
        self.sidebar.mainLayout.addStretch(1)
        layout.addWidget(self.sidebar)
        layout.addWidget(self.stacked)

        self.is_small = False
        self.window_small = False

        self.setCentralWidget(central_widget)

        signal_change.application_screen.connect(self.change_current_window)
        signal_change.limit_screen.connect(self.change_current_window)

    def toggle_sideboard(self):
        if not self.window_small:
            start_width = self.sidebar.width()
            end_width = 55 if not self.is_small else 200

            if self.cur_img_header == ":src/icon/left_panel_open.svg":
                self.button.setImage(":src/icon/left_panel_close.svg")
                self.cur_img_header = ":src/icon/left_panel_close.svg"
            else:
                self.button.setImage(":src/icon/left_panel_open.svg")
                self.cur_img_header = ":src/icon/left_panel_open.svg"

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

    def on_tray_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()
            self.activateWindow()

    def change_window(self, data: str):
        if data == "Обзор":
            self.stacked.setCurrentIndex(0)
        elif data == "Приложения":
            self.stacked.setCurrentIndex(1)
        elif data == "Лимиты":
            self.stacked.setCurrentIndex(2)
        elif data == "Фокус":
            self.stacked.setCurrentIndex(3)
        elif data == "Статистика":
            self.stacked.setCurrentIndex(4)
            stats_signal.upd_stats.emit()
        elif data == "История":
            self.stacked.setCurrentIndex(5)
            stats_signal.upd_history.emit()
        elif data == "Настройки":
            self.stacked.setCurrentIndex(6)

    def resizeEvent(self, event):
        width = self.width()

        if width < 856:
            if not self.is_small:
                self.toggle_sideboard()

            self.window_small = True

        if width > 856:
            self.window_small = False

            if self.window_small:
                self.logo.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def change_current_window(self, inx, data, types=None):
        self.stacked.setCurrentIndex(inx)

        if inx == 1:
            signal_change.application_arg.emit(data)

        if inx == 2:
            if types == 'category':
                signal_change.limit_category.emit(data)
            elif types == 'app':
                signal_change.limit_app.emit(data)