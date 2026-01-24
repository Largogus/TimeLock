from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout


class Wrapper(QHBoxLayout):
    def __init__(self, widget):
        super().__init__()

        self.addStretch(1)
        self.addWidget(widget)
        self.addStretch(1)