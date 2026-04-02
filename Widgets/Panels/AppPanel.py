from PySide6.QtGui import QColor
from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QMessageBox
from PySide6.QtCore import Qt
from Widgets.Buttons.Button import Button
from Widgets.Line import Line
from Widgets.Modal.CategoryModal import CategoryModal
from Widgets.Panels.PanelTemplate import PanelTemplate
from Widgets.Wrapper import Wrapper
from core.command.block_app import add_block_app, is_blocked, remove_block_app
from core.db.session import SessionLocal
from core.signals.change_signals import signal_change
from core.signals.notification_signals import show_notification
from core.statistic.clear_app_in_stat import clear_app_in_stat
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
        self.app_id = None
        self.block = False

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

        self.not_visible.clicked.connect(lambda: self.on_delete(self.app, self.app_id))
        self.delete_stat.clicked.connect(lambda: self.on_remove_stats(self.app))
        self.block_button.clicked.connect(lambda: self.on_blocked(self.app))

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
        self.app_id = name.get("id")

        self.block = is_blocked(self.app, SessionLocal(), app_is_name=True)
        self.block_button.setText(
            "Разблокировать" if self.block else "Заблокировать")

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

    def on_delete(self, data, id):
        from core.command.dont_tracking import dont_tracking
        from Widgets.Modal.MessageTemplate import MessageTemplate
        modal = MessageTemplate(
            msg_icon=QMessageBox.Icon.Question,
            text=f"Вы уверены, что хотите перестать отслеживать {data}?",
            title="Оповещение", standard_btn=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if modal:
            db_session = SessionLocal()
            dont_tracking(db_session, id)
            show_notification.show_notification_app_not_tracking.emit(data)

    def on_remove_stats(self, data):
        from Widgets.Modal.MessageTemplate import MessageTemplate
        modal = MessageTemplate(
            msg_icon=QMessageBox.Icon.Question,
            text=f"Вы уверены, что хотите удалить всю статистику {data}?",
            title="Оповещение", standard_btn=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if modal:
            db_session = SessionLocal()
            state, message = clear_app_in_stat(db_session, data)

            MessageTemplate(
                msg_icon=QMessageBox.Icon.Information if state else QMessageBox.Icon.Warning,
                text=message,
                title="Оповещение"
            )

    def on_blocked(self, data):
        from Widgets.Modal.MessageTemplate import MessageTemplate
        modal = MessageTemplate(
            msg_icon=QMessageBox.Icon.Question,
            text=f"Вы уверены, что хотите {'заблокировать' if not self.block else 'разблокировать'} {data}?",
            title="Оповещение", standard_btn=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if modal:
            db_session = SessionLocal()

            if not self.block:
                add_block_app(data, db_session)
                self.block_button.setText("Разблокировать")
                self.block = True
            else:
                remove_block_app(data, db_session)
                self.block_button.setText("Заблокировать")
                self.block = False