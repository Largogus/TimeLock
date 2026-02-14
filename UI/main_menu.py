from PySide6.QtWidgets import QWidget, QListWidget
from core.signals.tracker_signals import SignalObject


class MainMenu(QWidget):
    def __init__(self, signal: SignalObject = None):
        super().__init__()

        self.small_list = QListWidget()
        self.small_list.setMaximumWidth(55)

        self.large_list = QListWidget()
        self.large_list.setMaximumWidth(200)

        self.small_list.setGeometry(55, self.height(), 0, 0)
        self.large_list.setGeometry(200, self.height(), 55, 0)

        # self.main_layout = QVBoxLayout()
        #
        # self.signal_object = signal
        #
        # self.add_application = Button.Button("Добавить приложение")
        # self.add_application.clicked.connect(self.change_window)
        #
        # self.topFrame = Frame.BaseFrame()
        # self.topFrame.addElement(self.add_application)
        # self.topFrame.addElement(Button.Button("Статистика"))
        # self.topFrame.addElement(Button.Button("Настройки"))
        #
        # self.main_layout.addWidget(self.topFrame)
        #
        # self.lowFrame = Table.Table()
        #
        # self.main_layout.addWidget(self.lowFrame)
        #
        # self.setLayout(self.main_layout)

    # def change_window(self):
    #     self.signal_object.change_window.emit("add_apl")