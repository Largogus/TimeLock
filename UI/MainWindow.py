from PySide6.QtWidgets import QMainWindow, QStackedWidget
from core.DesktopSize import DesktopSize
from UI.MainMenu import MainMenu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 900, 700)

        x, y = DesktopSize(self)

        self.move(x, y)

        self.stacked = QStackedWidget()

        self.stacked.addWidget(MainMenu())

        '''| ---- |'''

        self.setCentralWidget(self.stacked)