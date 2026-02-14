from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from Widgets.Panels.PanelTemplate import PanelTemplate
from Widgets.Wrapper import Wrapper


class AppPanel(PanelTemplate):
    def __init__(self, parent=None):
        super().__init__(parent, width=400)

        lay = QVBoxLayout()

        self.name_app = QLabel()
        wrapper = Wrapper(self.name_app)

        header = QHBoxLayout()

        font_label = self.name_app.font()
        font_label.setPointSize(15)
        self.name_app.setFont(font_label)

        header.addLayout(wrapper)
        header.addWidget(self.close_btn)

        lay.addLayout(header)
        lay.addStretch()

        self.setLayout(lay)

    def setDate(self, name: dict):
        self.name_app.setText(name.get("name", 'Unknown'))