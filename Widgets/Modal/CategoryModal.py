from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QFont, QIcon, QPalette, QColor
from PySide6.QtCore import Qt
from Widgets.ComboBoxes.PopUp import PopUp
from core.command.category_command import get_category
from core.system.desktop import DesktopSize
from core.system.config import FONT_FAMILY
from core.db.session import SessionLocal

from core.widgets.change_category import changeCategory


class CategoryModal(QWidget):
    def __init__(self, app):
        super().__init__()
        self.db_session = SessionLocal()

        font = QFont(FONT_FAMILY, 14)
        font.setBold(True)

        self.setFont(font)
        self.setWindowTitle("Изменение категории")
        self.setWindowIcon(QIcon(":src/image.png"))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))

        x, y = DesktopSize(self)

        self.move(x, y)

        self.raise_()

        lay = QVBoxLayout()

        self.app_name = app

        self.title = QLabel()
        self.title.setText(f"Выберите категорию для {self.app_name}")

        self.change_category = PopUp(placeholder="Выберите категорию", close_btn=False)

        self.change_category.addItems(get_category(self.db_session))

        self.change_category.currentTextChanged.connect(self.change)

        lay.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignHCenter)
        lay.addWidget(self.change_category, alignment=Qt.AlignmentFlag.AlignHCenter)
        lay.addStretch()

        self.setLayout(lay)
        self.setPalette(palette)

    def change(self):
        new_cat = self.change_category.currentText()
        changeCategory(self.app_name, new_cat)
        self.close()