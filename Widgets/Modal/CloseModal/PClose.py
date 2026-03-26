from PySide6.QtWidgets import QVBoxLayout, QLabel, QDialog
from PySide6.QtGui import QFont, QPalette, QColor, QKeyEvent
from PySide6.QtCore import Qt
from Widgets.Buttons.Button import Button
from Widgets.Modal.CloseModal.TemplateClose import TemplateClose
from core.system.config import FONT_FAMILY


class PCModal(TemplateClose):
    def __init__(self, *args):
        super().__init__(*args)

        self.title.setText(f"Компьютер  заблокирован\n"
                           f"Вы достигли лимита использования.\n"
                           f"Доступ будет восстановлен в 0:00.")

        self.btn = Button("Выключить ПК", align=Qt.AlignmentFlag.AlignCenter)
        self.btn.clicked.connect(self.close)
        self.btn.setBackgroundColor(QColor("#ef706b"))
        self.btn.setBackgroundHover(QColor("#f0918e"))
        self.btn.setBackgroundPressed(QColor("#f16a65"))

        self.btn_disabled = Button("Выключить лимит на ПК", align=Qt.AlignmentFlag.AlignCenter)
        self.btn_disabled.clicked.connect(self.close)
        self.btn_disabled.setBackgroundColor(QColor("#ef706b"))
        self.btn_disabled.setBackgroundHover(QColor("#f0918e"))
        self.btn_disabled.setBackgroundPressed(QColor("#f16a65"))

        self.btn_defer = Button("Отложить лимит на 5 минут", align=Qt.AlignmentFlag.AlignCenter)
        self.btn_defer.clicked.connect(self.close)
        self.btn_defer.setBackgroundColor(QColor("#ef706b"))
        self.btn_defer.setBackgroundHover(QColor("#f0918e"))
        self.btn_defer.setBackgroundPressed(QColor("#f16a65"))

        self.lay.addWidget(self.title)
        self.lay.addSpacing(10)
        self.lay.addWidget(self.btn)

        if not self.defer:
            self.lay.addWidget(self.btn_defer)

        self.lay.addWidget(self.btn_disabled)