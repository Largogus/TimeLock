from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from Widgets.Buttons.Button import Button
from Widgets.Modal.CloseModal.TemplateClose import TemplateClose


class LimitModal(TemplateClose):
    def __init__(self, app, *args):
        super().__init__(*args)

        self.title.setText(f"{app} заблокирован\nВы достигли лимита использования.\nДоступ будет восстановлен завтра.")

        self.btn = Button("Закрыть", align=Qt.AlignmentFlag.AlignCenter)
        self.btn.clicked.connect(self.close)
        self.btn.setBackgroundColor(QColor("#ef706b"))
        self.btn.setBackgroundHover(QColor("#f0918e"))
        self.btn.setBackgroundPressed(QColor("#f16a65"))

        self.btn_rollup = Button("Свернуть", align=Qt.AlignmentFlag.AlignCenter)
        self.btn_rollup.clicked.connect(self.close)
        self.btn_rollup.setBackgroundColor(QColor("#ef706b"))
        self.btn_rollup.setBackgroundHover(QColor("#f0918e"))
        self.btn_rollup.setBackgroundPressed(QColor("#f16a65"))

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

        self.lay.addWidget(self.btn_rollup)