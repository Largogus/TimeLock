from PySide6.QtWidgets import QWidget, QVBoxLayout
from Widgets import Button, Frame


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout()

        self.topFrame = Frame.BaseFrame()
        self.topFrame.addButton(Button.Button("Попа"))

        self.main_layout.addWidget(self.topFrame)

        self.setLayout(self.main_layout)