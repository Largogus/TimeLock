from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout


class Wrapper(QHBoxLayout):
    def __init__(self, widget):
        """:param widget - self.addWidget(widget)''"""
        super().__init__()

        self._widget = widget

        self.addStretch(1)
        self.addWidget(self._widget)
        self.addStretch(1)