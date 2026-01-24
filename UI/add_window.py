from PySide6.QtWidgets import QWidget, QVBoxLayout, QRadioButton, QSpacerItem, QSizePolicy
from core.signals.signal import SignalObject
from PySide6.QtCore import QTimer, Qt
from Widgets.Frame import BaseFrame
from Widgets.PopUp import PopUp
from Widgets.Button import Button
from Widgets.TextEdit import TextEdit
from PySide6.QtGui import QColor, QFont
from core.system.process import get_application
from style.radio_button_style import RadioStyle
from core.db.session import SessionLocal
from core.models.models import Blacklist, App


class AddWindow(QWidget):
    def __init__(self, signal: SignalObject = None):
        super().__init__()

        self.layout = QVBoxLayout()
        self.application_name_text = ""

        ''' -=-=-=-=-=-=-=-=-=-=-=- '''

        self.main = BaseFrame()

        self.popup_object = BaseFrame()
        self.popup_object.setMaximumHeight(60)
        self.bd = PopUp(border_radius=15, background=QColor("#B6B6B6"), item=[x for x in get_application().keys()],
                         slot_bg=QColor("#B6B6B6"), text="Выбрать из базы ▼", font_size=20)

        self.pop = PopUp(border_radius=15, background=QColor("#B6B6B6"), item=[x for x in get_application().keys()], slot_bg=QColor("#B6B6B6"), text="Выбрать из запущенных ▼", font_size=20)
        self.pop.addItemList(get_application())
        self.pop.TextToTextEdit.connect(self.editEditText)

        self.timer = QTimer()
        self.timer.timeout.connect(self.addList)
        self.timer.start(1000)

        self.popup_object.addElement(self.bd)
        self.popup_object.addElement(self.pop)

        self.main.addElement(self.popup_object)

        self.main.setMaximumHeight(100)

        ''' -=-=-=-=-=-=-=-=-=-=-=- '''

        self.menu = BaseFrame(QVBoxLayout())

        self.app_name = BaseFrame()
        self.app_name.setMaximumHeight(150)

        self.app_name_edit = TextEdit(max_char=20, placeholder="Название")
        self.app_name_edit.setFixedHeight(120)

        self.app_name.addElement(self.app_name_edit)

        self.radio_group = BaseFrame()
        self.radio_group.setMinimumHeight(80)
        self.radio_group.setMinimumWidth(450)
        self.radio_group.setMaximumHeight(100)
        self.radio_group.setBackgroundColor(QColor("#B6B6B6"))

        self.block = QRadioButton()
        self.block.setStyle(RadioStyle())
        self.block.setChecked(True)
        self.block.setText("Не отслеживать")
        self.block.setFont(QFont('Arial', 18))
        self.block.setToolTip('Выберите, чтобы время данного приложения не замерялось')

        self.unblock = QRadioButton()
        self.unblock.setStyle(RadioStyle())
        self.unblock.setText("Отслеживать")
        self.unblock.setFont(QFont('Arial', 18))
        self.unblock.setToolTip('Выберите, чтобы время данного приложения вновь замерялось')

        self.radio_group.addElement(self.block, alignment=Qt.AlignmentFlag.AlignCenter)
        self.radio_group.addElement(self.unblock, alignment=Qt.AlignmentFlag.AlignCenter)

        self.button_group = BaseFrame()

        self.app_add = Button("Добавить", font_size=25)
        self.app_add.clicked.connect(self.addException)
        self.app_add.setMaximumHeight(120)
        self.app_add.setMinimumHeight(80)

        self.button_group.mainLayout.setSpacing(100)

        self.app_cancel = Button("Отменить", font_size=25)
        self.app_cancel.setMaximumHeight(120)
        self.app_cancel.setMinimumHeight(80)

        self.button_group.addElement(self.app_add)
        self.button_group.addElement(self.app_cancel)

        self.menu.addElement(self.app_name)
        self.menu.mainLayout.addStretch()
        self.menu.addElement(self.radio_group)
        self.menu.addElement(self.button_group)

        ''' -=-=-=-=-=-=-=-=-=-=-=- '''

        self.layout.addWidget(self.main)
        self.layout.addWidget(self.menu)

        self.setLayout(self.layout)

    def addList(self):
        self.pop.addItemList(get_application())

    def editEditText(self, text):
        self.app_name_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_name_edit.setText(text)
        self.app_name_edit.update()

    def addException(self):
        text = self.app_name_edit.text()

        # if

        if not (text.isalpha() or text.isdigit()):
            self.app_name_edit.setError(True)
            self.bd.setError(True)

            return
        else:
            self.app_name_edit.setError(False)
            self.bd.setError(False)

        if self.block.isChecked():
            s = SessionLocal()

            # try:
            #     app = App(name=self.app_name_edit.text(),
            #               path=)
