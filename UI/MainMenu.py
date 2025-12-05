from PySide6.QtWidgets import QWidget, QVBoxLayout
from Widgets import Button, Frame, Table
from core.Signal import SignalObject


class MainMenu(QWidget):
    def __init__(self, signal: SignalObject = None):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.signal_object = signal

        self.add_application = Button.Button("Добавить приложение")
        self.add_application.clicked.connect(self.change_window)

        self.topFrame = Frame.BaseFrame()
        self.topFrame.addElement(self.add_application)
        self.topFrame.addElement(Button.Button("Статистика"))
        self.topFrame.addElement(Button.Button("Настройки"))

        self.main_layout.addWidget(self.topFrame)

        self.lowFrame = Table.Table()

        self.main_layout.addWidget(self.lowFrame)

        self.setLayout(self.main_layout)

    def change_window(self):
        self.signal_object.change_window.emit("add_apl")