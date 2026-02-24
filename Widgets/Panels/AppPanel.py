from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from Widgets.Buttons.Button import Button
from Widgets.Line import Line
from Widgets.Modal.CategoryModal import CategoryModal
from Widgets.Panels.PanelTemplate import PanelTemplate
from Widgets.Wrapper import Wrapper
from core.signals.change_signals import signal_change
from core.system.date import normal_time


class AppPanel(PanelTemplate):
    def __init__(self, parent=None):
        super().__init__(parent, width=460)

        lay = QVBoxLayout()

        font_label = self.font()
        font_label.setPointSize(15)
        font_label.setBold(True)
        self.setFont(font_label)

        self.app = ""

        self.name_app = QLabel()
        wrapper = Wrapper(self.name_app)

        header = QHBoxLayout()

        header.addLayout(wrapper)
        header.addWidget(self.close_btn)

        category_block = QHBoxLayout()

        self.category_app = QLabel()

        self.category_app_edit = Button(name="Изменить", radius=10, align=Qt.AlignmentFlag.AlignCenter, maxs=150, alpha=[75, 100, 125], font_color=QColor('white'))
        self.category_app_edit.setBackgroundColor(QColor('#a3c8a5'))
        self.category_app_edit.setBackgroundHover(QColor('#a3c8a5'))
        self.category_app_edit.setBackgroundPressed(QColor('#a3c8a5'))
        self.category_app_edit.clicked.connect(self.change_category)

        category_block.addWidget(self.category_app)
        category_block.addStretch(1)
        category_block.addWidget(self.category_app_edit)

        stat_block = QVBoxLayout()

        statistic = QLabel("Статистика:")

        stat_block.addLayout(Wrapper(statistic))

        self.statistic_today = QLabel()
        self.statistic_for_seven_day = QLabel()

        stat_block.addWidget(self.statistic_today)
        stat_block.addWidget(self.statistic_for_seven_day)

        limit_head = QLabel("Лимит времени:")

        limit_block = QHBoxLayout()

        self.limit_title = QLabel()
        self.limit_button = Button(name="", radius=10, align=Qt.AlignmentFlag.AlignCenter, maxs=150, alpha=[75, 100, 125], font_color=QColor('white'))

        self.limit_button.setBackgroundColor(QColor('#a3c8a5'))
        self.limit_button.setBackgroundHover(QColor('#a3c8a5'))
        self.limit_button.setBackgroundPressed(QColor('#a3c8a5'))

        limit_block.addWidget(self.limit_title)
        limit_block.addWidget(self.limit_button)

        block_title = QLabel("Ограничения")

        self.block_button = Button(name="Заблокировать", radius=10, align=Qt.AlignmentFlag.AlignCenter,
                                   maxs=150, alpha=[75, 100, 125], font_color=QColor('white'))

        self.block_button.setBackgroundColor(QColor('#a3c8a5'))
        self.block_button.setBackgroundHover(QColor('#a3c8a5'))
        self.block_button.setBackgroundPressed(QColor('#a3c8a5'))

        block_label = QLabel()
        block_label.setText("Приложение нельзя будет запустить, пока вы не разблокируете его вручную")
        block_font = block_label.font()
        block_font.setPointSize(8)
        block_label.setFont(block_font)

        self.not_visible = Button(name="Не отслеживать", radius=10, align=Qt.AlignmentFlag.AlignCenter,
                                   maxs=500, alpha=[75, 100, 125], font_color=QColor('white'))
        self.delete_stat = Button(name="Сбросить статистику", radius=10, align=Qt.AlignmentFlag.AlignCenter, maxs=500,
                                   alpha=[75, 100, 125], font_color=QColor('white'))

        self.not_visible.setBackgroundColor(QColor('#6B7280'))
        self.not_visible.setBackgroundHover(QColor('#6B7280'))
        self.not_visible.setBackgroundPressed(QColor('#6B7280'))

        self.delete_stat.setBackgroundColor(QColor('#6B7280'))
        self.delete_stat.setBackgroundHover(QColor('#6B7280'))
        self.delete_stat.setBackgroundPressed(QColor('#6B7280'))

        lay.addLayout(header)
        lay.addWidget(Line("H"))
        lay.addLayout(category_block)
        lay.addWidget(Line("H"))
        lay.addLayout(stat_block)
        lay.addWidget(Line("H"))
        lay.addLayout(Wrapper(limit_head))
        lay.addLayout(limit_block)
        lay.addWidget(Line("H"))
        lay.addLayout(Wrapper(block_title))
        lay.addLayout(Wrapper(self.block_button))
        lay.addLayout(Wrapper(block_label))
        lay.addWidget(Line("H"))
        lay.addStretch()
        lay.addLayout(Wrapper(self.not_visible))
        lay.addLayout(Wrapper(self.delete_stat))

        lay.addStretch()

        self.setLayout(lay)

    def setDate(self, name: dict):
        self.app = name.get("name", 'Unknown')
        self.name_app.setText(name.get("name", 'Unknown'))
        self.category_app.setText(f'Категория: {name.get("category", "Unknown")}')
        self.statistic_today.setText(f'Сегодня: {name.get("today", "Unknown")}')
        self.statistic_for_seven_day.setText(f'Среднее за неделю: {normal_time((name.get("middle_time", "Unknown")), "short")}')

        limit = (name.get("limit", "Unknown"))
        self.limit_title.setText(f'Лимит: {limit if limit != "Нет" else "не установлен"}')

        self.limit_button.clicked.connect(lambda: signal_change.limit_screen.emit(2, self.name_app.text(), "app"))

        if limit == "Нет":
            self.limit_button.setText("Установить лимит")
        else:
            self.limit_button.setText("Изменить лимит")

    def change_category(self):
        self.category_modal = CategoryModal(self.app)

        self.category_modal.show()