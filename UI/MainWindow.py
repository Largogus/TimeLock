from PySide6.QtWidgets import QMainWindow, QStackedWidget
from core.DesktopSize import DesktopSize
from core.Signal import SignalObject
from UI.MainMenu import MainMenu
from UI.AddWindow import AddWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 900, 700)
        self.setWindowTitle('TimeLock')

        self.signal = SignalObject()
        self.signal.change_window.connect(self.change_window)

        x, y = DesktopSize(self)

        self.move(x, y)

        self.stacked = QStackedWidget()

        self.stacked.addWidget(MainMenu(self.signal))
        self.stacked.addWidget(AddWindow(self.signal))

        self.setCentralWidget(self.stacked)

    def change_window(self, data):
        if data == "main_window":
            self.stacked.setCurrentIndex(0)
        elif data == "add_apl":
            self.stacked.setCurrentIndex(1)
        elif data == "statistic":
            self.stacked.setCurrentIndex(2)
        elif data == "settings":
            self.stacked.setCurrentIndex(3)