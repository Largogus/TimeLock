from PySide6.QtCore import Qt, QTimer, QTime
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QTimeEdit, QHBoxLayout, \
    QCompleter, QMessageBox

from Style.PopupStyle import PopupStyle
from Widgets.Buttons.Button import Button
from Widgets.Completer import Completer
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from Widgets.ComboBoxes.PopUp import PopUp
from Widgets.TextsEdits.TextEdit import TextEdit
from core.command.category_command import get_category, count_time_category, count_limit_category
from core.command.edit_limit import edit_limit_app, edit_limit_category, delete_limit_app, delete_limit_category, \
    get_category_limit, turn_category_limit, turn_app_limit, get_app_limit
from core.command.get_all_app import get_all_app, count_time_app_name, count_limit_app_name
from core.command.is_exists_in_bd import is_exists_in_bd
from core.command.settings import set_settings
from core.db.session import SessionLocal
from core.signals.change_signals import signal_change
from core.signals.core_events import core_events
from core.signals.edit_signals import signal_edit
from core.signals.notification_signals import show_notification
from core.system.config import SETTINGS
from core.system.date import normal_time, time_for_qt
from core.system.get_total_pc_time_today import get_total_pc_time_today


class Limit(QWidget):
    def __init__(self):
        super().__init__()

        self.db_session = SessionLocal()

        layout = QVBoxLayout()
        layout.addSpacing(-20)

        self.main = BaseFrame(QVBoxLayout())
        self.main.mainLayout.setContentsMargins(20, 20, 20, 0)
        self.main.setBorderRadius(0)

        title = QLabel()
        title_font = title.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setPalette(QPalette(QColor(255, 255, 255)))
        title.setText('Лимиты')

        info_window = QLabel()
        info_window.setText("Управление ограничениями времени")
        info_window.setPalette(QPalette(QColor(163, 163, 163)))
        info_window_font = info_window.font()
        info_window_font.setPointSize(14)
        info_window.setFont(info_window_font)

        self.main.addElement(title)
        self.main.addElement(info_window)

        self.main.addElement(Line('H'))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(4, 4)

        common_limit_block = BaseFrame(box=QVBoxLayout(), border=14)
        common_limit_block.setBackgroundColor(QColor("#FFFFFF"))

        common_limit_block_font = common_limit_block.font()
        common_limit_block_font.setPointSize(14)
        common_limit_block_font.setBold(True)

        common_limit_block.setFont(common_limit_block_font)

        common_limit_block.setGraphicsEffect(shadow)

        common_limit_block_vbox = QVBoxLayout()

        common_limit_block_hbox = QHBoxLayout()

        palette_label = QPalette()
        palette_label.setColor(QPalette.ColorRole.WindowText, QColor("black"))

        common_limit_text = QLabel()
        common_limit_text_font = common_limit_text.font()
        common_limit_text_font.setPointSize(16)
        common_limit_text.setText("Общий дневной лимит")
        common_limit_text.setPalette(palette_label)
        common_limit_text.setFont(common_limit_text_font)

        self.common_limit_text_db = QLabel()
        self.common_limit_text_db.setPalette(palette_label)

        self.picker = QTimeEdit()
        self.picker.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.picker.setButtonSymbols(QTimeEdit.ButtonSymbols.NoButtons)
        self.picker.setMinimumWidth(120)
        self.picker.setMinimumHeight(50)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#F2F4F6"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#111827"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#27AE60"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        self.picker.setPalette(palette)

        btn_group = QHBoxLayout()

        save_btn = Button(name="Сохранить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10, maxs=250)
        save_btn.setBackgroundColor(QColor("#7adca3"))
        save_btn.setBackgroundHover(QColor("#52e08d"))
        save_btn.setBackgroundPressed(QColor("#1fad5a"))
        save_btn.clicked.connect(self.setLimitCommon)

        self.turn_btn = Button(name="", align=Qt.AlignmentFlag.AlignCenter, radius=10, maxs=250,
                               disabled_text="Лимит на ПК отсутсвует")
        self.turn_btn.setBackgroundColor(QColor("#a9d6bc"))
        self.turn_btn.setBackgroundHover(QColor("#aedbc1"))
        self.turn_btn.setBackgroundPressed(QColor("#b7e1c8"))
        self.turn_btn.clicked.connect(self.turnLimitCommon)
        self.get_turn()

        self.del_btn = Button(name="Удалить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10, maxs=250,
                               disabled_text="Лимит на ПК отсутсвует")
        self.del_btn.setBackgroundColor(QColor("#bdcbc3"))
        self.del_btn.setBackgroundHover(QColor("#a9bcb1"))
        self.del_btn.setBackgroundPressed(QColor("#85a391"))
        self.del_btn.clicked.connect(self.removeLimitCommon)

        btn_group.addWidget(save_btn)
        btn_group.addWidget(self.turn_btn)
        btn_group.addWidget(self.del_btn)

        common_limit_block_vbox.addWidget(common_limit_text)
        common_limit_block_vbox.addWidget(self.common_limit_text_db)
        common_limit_block_vbox.addLayout(btn_group)

        common_limit_block_hbox.addLayout(common_limit_block_vbox)
        common_limit_block_hbox.addStretch()
        common_limit_block_hbox.addWidget(self.picker)
        common_limit_block_hbox.addStretch()

        common_limit_block.addLayout(common_limit_block_hbox)
        self.updateTextCommonLimit()

        self.main.addElement(common_limit_block)
        self.main.addElement(Line('H'))

        '''------------------------------------------------'''

        category_limit_block = BaseFrame(box=QVBoxLayout(), border=14)
        category_limit_block.setBackgroundColor(QColor("#FFFFFF"))

        category_limit_block_hbox = QHBoxLayout()
        category_limit_block_vbox = QVBoxLayout()

        category_limit_block_font = common_limit_block.font()
        category_limit_block_font.setPointSize(14)
        category_limit_block_font.setBold(True)

        category_limit_block.setFont(category_limit_block_font)

        category_limit_block.setGraphicsEffect(shadow)

        category_limit_text = QLabel()
        category_limit_text_font = category_limit_text.font()
        category_limit_text_font.setPointSize(16)
        category_limit_text.setText("Лимиты категорий")
        category_limit_text.setPalette(palette_label)
        category_limit_text.setFont(category_limit_text_font)

        categories = get_category(self.db_session)
        self.category_limit_popup = PopUp(placeholder="Выберите категорию")
        self.category_limit_popup.addItems(categories)
        self.category_limit_popup.currentTextChanged.connect(self.set_category_block)

        core_events.remove_category.connect(lambda category: self.category_limit_popup.removeItem(self.remove_for_index(categories, category)))
        core_events.add_category.connect(lambda category: self.add_item(categories, category))
        core_events.rename_category.connect(lambda category, new: self.rename_elm(categories, category, new))

        self.category_limit_today = QLabel()
        self.category_limit_today.setText(f"Сегодня: —")
        self.category_limit_today.setPalette(palette_label)

        self.category_limit_limit = QTimeEdit()
        self.category_limit_limit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_limit_limit.setButtonSymbols(QTimeEdit.ButtonSymbols.NoButtons)
        self.category_limit_limit.setTime(time_for_qt(0))
        self.category_limit_limit.setMinimumWidth(120)
        self.category_limit_limit.setMinimumHeight(50)
        self.category_limit_limit.setPalette(palette)

        btn_group_category = QHBoxLayout()

        self.category_limit_edit = Button(name="Сохранить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10,
                                          maxs=250, disabled_text="Выберите категорию для действия")
        self.category_limit_edit.setBackgroundColor(QColor("#a8f0c6"))
        self.category_limit_edit.setBackgroundHover(QColor("#52e08d"))
        self.category_limit_edit.setBackgroundPressed(QColor("#1fad5a"))

        self.category_limit_edit.clicked.connect(self.setLimitCategory)

        self.turn_category_limit = Button(name="Отключить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10,
                                          maxs=250,  disabled_text="Выберите категорию для действия")
        self.turn_category_limit.setBackgroundColor(QColor("#a9d6bc"))
        self.turn_category_limit.setBackgroundHover(QColor("#aedbc1"))
        self.turn_category_limit.setBackgroundPressed(QColor("#b7e1c8"))
        self.turn_category_limit.clicked.connect(self.turnCategotyBlock)

        self.delete_category_limit = Button(name="Удалить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10,
                                            maxs=250, disabled_text="Выберите категорию для действия")
        self.delete_category_limit.setBackgroundColor(QColor("#bdcbc3"))
        self.delete_category_limit.setBackgroundHover(QColor("#a9bcb1"))
        self.delete_category_limit.setBackgroundPressed(QColor("#85a391"))
        self.delete_category_limit.clicked.connect(self.removeLimitCategory)

        btn_group_category.addWidget(self.category_limit_edit)
        btn_group_category.addWidget(self.turn_category_limit)
        btn_group_category.addWidget(self.delete_category_limit)

        self.category_limit_edit.setDisabled(True)
        self.turn_category_limit.setDisabled(True)
        self.delete_category_limit.setDisabled(True)

        self.category_limit_limit.setDisabled(True)

        self.category_limit_popup.close.connect(self.reset_category_block)

        category_limit_block_vbox.addWidget(category_limit_text)
        category_limit_block_vbox.addWidget(self.category_limit_popup)
        category_limit_block_vbox.addWidget(self.category_limit_today)
        category_limit_block_vbox.addLayout(btn_group_category)

        category_limit_block_hbox.addLayout(category_limit_block_vbox)
        category_limit_block_hbox.addStretch()
        category_limit_block_hbox.addWidget(self.category_limit_limit)
        category_limit_block_hbox.addStretch()

        category_limit_block.addLayout(category_limit_block_hbox)

        '''------------------------------------------------'''

        app_limit_block = BaseFrame(box=QVBoxLayout(), border=14)
        app_limit_block.setBackgroundColor(QColor("#FFFFFF"))

        app_limit_block_hbox = QHBoxLayout()
        app_limit_block_vbox = QVBoxLayout()

        app_limit_block_font = common_limit_block.font()
        app_limit_block_font.setPointSize(14)
        app_limit_block_font.setBold(True)

        app_limit_block.setFont(category_limit_block_font)

        app_limit_block.setGraphicsEffect(shadow)

        app_limit_text = QLabel()
        app_limit_text_font = category_limit_text.font()
        app_limit_text_font.setPointSize(16)
        app_limit_text.setText("Лимиты приложений")
        app_limit_text.setPalette(palette_label)
        app_limit_text.setFont(category_limit_text_font)

        self.app_limit_text_edit = TextEdit(image=":src/icon/search.svg", placeholder="Найти приложение...", ratio=0.60)
        self.app_limit_text_edit.textChanged.connect(self.on_text_changed)
        self.app_limit_text_edit.setMinimumHeight(35)
        self.app_limit_text_edit.setMaximumWidth(336)
        apps_completer = get_all_app(self.db_session)

        completer = Completer(self.app_limit_text_edit, apps_completer)
        popup = completer.popup()
        popup.setAutoFillBackground(False)
        popup.setItemDelegate(PopupStyle(bg=QColor("#e0e0e0"), hbg=QColor(166, 217, 166, 255), clc_bg=QColor("#b4e9b4"), text_color=QColor("black")))
        popup.setLineWidth(0)

        core_events.app_added.connect(lambda name: update_completer(name, completer, apps_completer))

        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.do_search)

        self.app_limit_today = QLabel()
        self.app_limit_today.setText(f"Сегодня: —")
        self.app_limit_today.setPalette(palette_label)

        self.app_limit_limit = QTimeEdit()
        self.app_limit_limit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_limit_limit.setButtonSymbols(QTimeEdit.ButtonSymbols.NoButtons)
        self.app_limit_limit.setTime(time_for_qt(0))
        self.app_limit_limit.setMinimumWidth(120)
        self.app_limit_limit.setMinimumHeight(50)
        self.app_limit_limit.setPalette(palette)

        btn_group_app = QHBoxLayout()

        self.app_limit_edit = Button(name="Сохранить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10, maxs=250,
                                     disabled_text="Выберите приложение для действия")

        self.app_limit_edit.setBackgroundColor(QColor("#a8f0c6"))
        self.app_limit_edit.setBackgroundHover(QColor("#52e08d"))
        self.app_limit_edit.setBackgroundPressed(QColor("#1fad5a"))

        self.app_limit_edit.clicked.connect(self.setLimitApp)

        self.turn_app_limit = Button(name="Отключить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10, maxs=250,
                                     disabled_text="Выберите приложение для действия")
        self.turn_app_limit.setBackgroundColor(QColor("#a9d6bc"))
        self.turn_app_limit.setBackgroundHover(QColor("#aedbc1"))
        self.turn_app_limit.setBackgroundPressed(QColor("#b7e1c8"))
        self.turn_app_limit.clicked.connect(self.turnAppBlock)

        self.delete_app_limit = Button(name="Удалить лимит", align=Qt.AlignmentFlag.AlignCenter, radius=10, maxs=250,
                                       disabled_text="Выберите приложение для действия")
        self.delete_app_limit.setBackgroundColor(QColor("#bdcbc3"))
        self.delete_app_limit.setBackgroundHover(QColor("#a9bcb1"))
        self.delete_app_limit.setBackgroundPressed(QColor("#85a391"))
        self.delete_app_limit.clicked.connect(self.removeLimitApp)

        btn_group_app.addWidget(self.app_limit_edit)
        btn_group_app.addWidget(self.turn_app_limit)
        btn_group_app.addWidget(self.delete_app_limit)

        self.app_limit_edit.setDisabled(True)
        self.turn_app_limit.setDisabled(True)
        self.delete_app_limit.setDisabled(True)

        self.app_limit_limit.setDisabled(True)

        # self.app_limit_popup.close.connect(self.reset_category_block)

        app_limit_block_vbox.addWidget(app_limit_text)
        app_limit_block_vbox.addWidget(self.app_limit_text_edit)
        app_limit_block_vbox.addWidget(self.app_limit_today)
        app_limit_block_vbox.addLayout(btn_group_app)

        app_limit_block_hbox.addLayout(app_limit_block_vbox)
        app_limit_block_hbox.addStretch()
        app_limit_block_hbox.addWidget(self.app_limit_limit)
        app_limit_block_hbox.addStretch()

        app_limit_block.addLayout(app_limit_block_hbox)

        """--------------------------------------------------------"""

        self.main.addElement(category_limit_block)
        self.main.addElement(Line("H"))
        self.main.addElement(app_limit_block)

        self.main.mainLayout.addStretch()

        layout.addWidget(self.main)
        layout.addSpacing(-20)

        self.setLayout(layout)

        signal_change.limit_category.connect(self.category_limit_popup.setCurrentText)
        signal_change.limit_app.connect(self.app_limit_text_edit.setText)
        signal_edit.upd_limit.connect(self.updateTextCommonLimit)

    def reset_category_block(self):
        self.category_limit_today.setText(f"Сегодня: —")
        self.turn_category_limit.setText(f"Отключить лимит")
        self.category_limit_edit.setDisabled(True)
        self.turn_category_limit.setDisabled(True)
        self.delete_category_limit.setDisabled(True)
        self.category_limit_limit.setDisabled(True)

    def set_category_block(self, category):
        today_time = normal_time(count_time_category(self.db_session, category), 'short')
        limit_cat = count_limit_category(self.db_session, category)

        if limit_cat is None: limit_cat = 0

        self.category_limit_today.setText(f"Сегодня: {today_time} из {normal_time(limit_cat, 'short')}" if limit_cat else f'Сегодня: {today_time}')
        self.category_limit_limit.setTime(time_for_qt(limit_cat))

        category_limit, is_limit = get_category_limit(self.db_session, category)

        if is_limit != 0 and is_limit is not None:
            self.turn_category_limit.setText("Включить лимит" if category_limit == 0 else "Отключить лимит")
            self.turn_category_limit.setDisabled(False)
            self.turn_category_limit.setDisabledText("Выберите категорию для действия")
        else:
            self.turn_category_limit.setText("Включить лимит" if category_limit == 0 else "Отключить лимит")
            self.turn_category_limit.setDisabled(True)
            self.turn_category_limit.setDisabledText("У вас нет лимита на эту категорию")

        self.category_limit_limit.setDisabled(False)
        self.category_limit_edit.setDisabled(False)
        self.delete_category_limit.setDisabled(False)

    def turnCategotyBlock(self):
        category = self.category_limit_popup.currentText()
        turn = turn_category_limit(self.db_session, category)

        if turn:
            self.set_category_block(category)
            return

    def turnAppBlock(self):
        app = self.app_limit_text_edit.text()
        turn = turn_app_limit(self.db_session, app)

        if turn:
            self.do_search()
            return

    def on_text_changed(self, text):
        self.search_timer.start(250)

    def do_search(self):
        app_name = self.app_limit_text_edit.text()

        exist = is_exists_in_bd(self.db_session, app_name)

        if not exist:
            self.app_limit_today.setText(f"Сегодня: —")
            self.app_limit_limit.setTime(time_for_qt(0))
            self.app_limit_limit.setDisabled(True)
            self.app_limit_edit.setDisabled(True)
            self.delete_app_limit.setDisabled(True)

            return

        today = normal_time(count_time_app_name(self.db_session, app_name))
        count_lim = count_limit_app_name(self.db_session, app_name)

        if count_lim is None: count_lim = 0

        self.app_limit_today.setText(f"Сегодня: {today} из {normal_time(count_lim, 'short')}" if count_lim else f'Сегодня: {today}')
        self.app_limit_limit.setTime(time_for_qt(count_lim))
        self.app_limit_limit.setDisabled(False)
        self.app_limit_edit.setDisabled(False)

        category_limit, is_limit = get_app_limit(self.db_session, app_name)

        if is_limit != 0 and is_limit is not None:
            self.turn_app_limit.setText("Включить лимит" if category_limit == 0 else "Отключить лимит")
            self.turn_app_limit.setDisabled(False)
            self.delete_app_limit.setDisabled(False)
            self.turn_app_limit.setDisabledText("Выберите приложение для действия")
        else:
            self.turn_app_limit.setText("Включить лимит" if category_limit == 0 else "Отключить лимит")
            self.turn_app_limit.setDisabled(True)
            self.delete_app_limit.setDisabled(True)
            self.turn_app_limit.setDisabledText("У вас нет лимита на это приложение")

    def setLimitApp(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        time = self.app_limit_limit.time()
        seconds = QTime(0, 0).secsTo(time)
        app_name = self.app_limit_text_edit.text()

        if seconds == 0:
            self.removeLimitApp()
            return

        if seconds < 5 * 60:
            show_notification.show_notification_error_limit.emit("приложений", 5)
            return

        edit = edit_limit_app(self.db_session, app_name, seconds)

        if edit:
            MessageTemplate(title="Оповещение", text=f"Лимит для {app_name} успешно изменён", msg_icon=QMessageBox.Icon.Information)
            self.do_search()

            return

    def setLimitCategory(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        time = self.category_limit_limit.time()
        seconds = QTime(0, 0).secsTo(time)
        app_name = self.category_limit_popup.currentText()

        if seconds == 0:
            self.removeLimitCategory()
            return

        if seconds < 10 * 60:
            show_notification.show_notification_error_limit.emit("категорий", 10)
            return

        edit = edit_limit_category(self.db_session, app_name, seconds)

        if edit:
            MessageTemplate(title="Оповещение", text=f"Лимит для {app_name} успешно изменён", msg_icon=QMessageBox.Icon.Information)
            self.set_category_block(app_name)

            return

    def removeLimitApp(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        app_name = self.app_limit_text_edit.text()

        edit = delete_limit_app(self.db_session, app_name)

        if edit:
            MessageTemplate(title="Оповещение", text=f"Лимит для {app_name} успешно удалён", msg_icon=QMessageBox.Icon.Information)
            self.do_search()

            return

    def removeLimitCategory(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        app_name = self.category_limit_popup.currentText()

        edit = delete_limit_category(self.db_session, app_name)

        if edit:
            MessageTemplate(title="Оповещение", text=f"Лимит для {app_name} успешно удалён", msg_icon=QMessageBox.Icon.Information)
            self.set_category_block(app_name)

            return

    def setLimitCommon(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        time = self.picker.time()
        seconds = QTime(0, 0).secsTo(time)

        if seconds == 0:
            self.removeLimitCommon()
            return

        if seconds < 30 * 60:
            show_notification.show_notification_error_limit.emit("ПК", 30)
            return

        edit = set_settings(self.db_session, "total_limit_pc", seconds, int)

        if edit:
            MessageTemplate(title="Оповещение", text=f"Лимит для компьютера успешно изменён", msg_icon=QMessageBox.Icon.Information)
            self.updateTextCommonLimit()

            return

    def turnLimitCommon(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        state = SETTINGS.get("state_limit_pc", 1)
        edit = set_settings(self.db_session, "state_limit_pc", not bool(state), int)

        if edit:
            if state == 0:
                text = "включён"
                self.turn_btn.setText("Отключить лимит")
            else:
                text = "отключён"
                self.turn_btn.setText("Включить лимит")

            MessageTemplate(title="Оповещение", text=f"Лимит для компьютера успешно {text}", msg_icon=QMessageBox.Icon.Information)

            return

    def get_turn(self):
        state = SETTINGS.get("state_limit_pc", 1)

        if state == 1:
            self.turn_btn.setText("Отключить лимит")
        else:
            self.turn_btn.setText("Включить лимит")

    def removeLimitCommon(self):
        from Widgets.Modal.MessageTemplate import MessageTemplate

        edit = set_settings(self.db_session, "total_limit_pc", 0, int)

        if edit:
            signal_edit.edit_or_delete_common_limit.emit(edit)
            MessageTemplate(title="Оповещение", text=f"Лимит для компьютера успешно удалён", msg_icon=QMessageBox.Icon.Information)
            self.updateTextCommonLimit()

            return

    def updateTextCommonLimit(self):
        common_limit_time = SETTINGS.get("total_limit_pc", 0)

        if common_limit_time == 0:
            self.turn_btn.setDisabled(True)
            self.del_btn.setDisabled(True)
        else:
            self.turn_btn.setDisabled(False)
            self.del_btn.setDisabled(False)

        common_limit_str = normal_time(common_limit_time, "short")

        today_time_str = normal_time(get_total_pc_time_today(), "short")

        signal_edit.edit_or_delete_common_limit.emit(common_limit_time)

        self.common_limit_text_db.setText(f"Сегодня: {today_time_str} из {common_limit_str}" if common_limit_time != 0 else "Без лимита")
        self.picker.setTime(time_for_qt(common_limit_time))

    def remove_for_index(self, lists: list, category):
        zn = lists.index(category)
        lists.pop(zn)
        return zn

    def add_item(self, lists: list, category):
        lists.append(category)
        self.category_limit_popup.addItem(category)

    def rename_elm(self, lists: list, last, new):
        inx = lists.index(last)
        lists.pop(inx)
        self.category_limit_popup.removeItem(inx)
        lists.append(new)
        self.category_limit_popup.addItem(new)


def update_completer(name, completer, app_list):
    app_list.append(name)
    completer.update_items(app_list)