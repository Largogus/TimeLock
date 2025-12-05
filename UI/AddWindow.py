from PySide6.QtWidgets import QWidget, QVBoxLayout
from core.Signal import SignalObject
from PySide6.QtCore import QTimer, Qt
from Widgets.Frame import BaseFrame
from Widgets.PopUp import PopUp
from Widgets.Button import Button
from Widgets.TextEdit import TextEdit
from PySide6.QtGui import QColor
from core.Process import get_application


class AddWindow(QWidget):
    def __init__(self, signal: SignalObject = None):
        super().__init__()

        self.layout = QVBoxLayout()

        self.main = BaseFrame()

        self.more_button = Button('Обзор', 20, 0, 200)

        self.popup_object = BaseFrame()
        self.popup_object.setMaximumHeight(60)

        self.application_name_text = ""

        self.pop = PopUp(border_radius=15, background=QColor("#B6B6B6"), item=get_application().values(), slot_bg=QColor("#B6B6B6"), text="Выбрать из запущенных ▼", font_size=20)
        self.pop.addItemList(get_application().values())
        self.pop.TextToTextEdit.connect(self.editEditText)

        self.timer = QTimer()
        self.timer.timeout.connect(self.addList)
        self.timer.start(1000)

        self.popup_object.addElement(self.pop)

        self.main.addElement(self.more_button)
        self.main.addElement(self.popup_object)

        self.main.setMaximumHeight(100)

        self.menu = BaseFrame()

        self.app_name = BaseFrame()
        self.app_name.setMaximumHeight(150)

        self.app_name_edit = TextEdit(max_char=20, place="Название")
        self.app_name_edit.setMaximum(150)

        self.app_name.addElement(self.app_name_edit)
        self.menu.addElement(self.app_name)

        self.layout.addWidget(self.main)
        self.layout.addWidget(self.menu)

        self.setLayout(self.layout)

    def addList(self):
        self.pop.addItemList(get_application().values())

    def editEditText(self, text):
        self.app_name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_name_edit.setText(text)
        self.app_name_edit.update()