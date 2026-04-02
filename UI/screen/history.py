from PySide6.QtCore import QStringListModel
from PySide6.QtGui import QColor, QPalette, QFont, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QScrollArea, QCompleter
from Style.PopupStyle import PopupStyle
from Widgets.Cards.HistoryCard import HistoryCard
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from Widgets.TextsEdits.TextEdit import TextEdit
from Widgets.Wrapper import Wrapper
from core.db.session import SessionLocal
from core.signals.statistics_signsl import stats_signal
from core.statistic.history_stats import get_history_session
from core.system.config import FONT_FAMILY
from core.system.date import normal_time
from core.thread.stat.get_stat_info import StatisticThread
from core.widgets.thread_manager import thread_manager


class History(QWidget):
    def __init__(self):
        super().__init__()

        self.db_session = SessionLocal()

        self.thread_stat = thread_manager.register(StatisticThread(SessionLocal))
        self.thread_stat.start()

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
        title.setText('История')

        info_window = QLabel()
        info_window.setText("Что вы делали сегодня за компьютером")
        info_window.setPalette(QPalette(QColor(163, 163, 163)))
        info_window_font = info_window.font()
        info_window_font.setPointSize(14)
        info_window.setFont(info_window_font)

        self.main.addElement(title)
        self.main.addElement(info_window)

        self.main.addElement(Line('H'))

        '''|---------------------------------------------|'''

        self.palette_label = QPalette()
        self.palette_label.setColor(QPalette.ColorRole.Text, QColor("black"))
        self.palette_label.setColor(QPalette.ColorRole.WindowText, QColor("black"))

        self.font_label = QFont(FONT_FAMILY, 16)
        self.font_label.setBold(True)

        h_list = QHBoxLayout()

        self.left_part = BaseFrame(QVBoxLayout())

        self.left_part.setMinimumWidth(500)

        h_list.addWidget(self.left_part)

        self.title_left_part = QLabel()
        self.title_left_part.setText("Лента истории")
        self.title_left_part.setPalette(self.palette_label)
        self.title_left_part.setFont(self.font_label)

        self.text_edit = TextEdit(image=":src/icon/search.svg", placeholder="Найти приложение...", ratio=0.40)
        self.text_edit.textChanged.connect(self.on_text_changed)
        self.text_edit.setMinimumHeight(35)
        self.text_edit.setMaximumWidth(1000)

        """~~~~~~~~~~~~~~~~~~~~~~~~~"""

        self.scroll_wrapper = QScrollArea()
        self.scroll_wrapper.setWidgetResizable(True)

        self.widget = QWidget()

        widg_palette = self.scroll_wrapper.palette()
        widg_palette.setColor(QPalette.ColorRole.Base, QColor('#CFCFCF'))
        widg_palette.setColor(QPalette.ColorRole.Window, QColor('#CFCFCF'))

        self.history_dict = {}

        self.model = QStringListModel([])

        self.lay = QVBoxLayout()

        self.lay.addStretch()

        self.widget.setLayout(self.lay)

        completer = QCompleter()
        completer.setModel(self.model)
        completer.setWidget(self.text_edit)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        popup = completer.popup()
        popup.setAutoFillBackground(False)
        popup.setItemDelegate(PopupStyle(bg=QColor("#e0e0e0"), hbg=QColor(166, 217, 166, 255), clc_bg=QColor("#b4e9b4"),
                                         text_color=QColor("black")))

        self.text_edit.setCompleter(completer)

        self.scroll_wrapper.setWidget(self.widget)
        self.scroll_wrapper.setPalette(widg_palette)

        """~~~~~~~~~~~~~~~~~~~~~~~~~"""

        self.left_part.addLayout(Wrapper(self.title_left_part))
        self.left_part.addElement(self.text_edit)
        self.left_part.addElement(self.scroll_wrapper)

        self.left_part.setMinimumHeight(500)
        self.left_part.setMaximumHeight(1080)

        h_list.addWidget(Line('V'))

        self.right_part = BaseFrame(QVBoxLayout())

        self.title_right_part = QLabel()
        self.title_right_part.setText("Детали")
        self.title_right_part.setFont(self.font_label)
        self.title_right_part.setPalette(self.palette_label)

        self.title_app = QLabel()
        self.title_app.setText("Выберите приложение")
        self.title_app.setFont(self.font_label)
        self.title_app.setPalette(self.palette_label)

        self.scroll_details = QScrollArea()
        self.scroll_details.setWidgetResizable(True)

        details_palette = self.scroll_details.palette()
        details_palette.setColor(QPalette.ColorRole.Base, QColor('#dedede'))
        details_palette.setColor(QPalette.ColorRole.Window, QColor('#dedede'))

        self.scroll_details.setPalette(details_palette)

        self.widget_details = QWidget()

        self.lay_details = QVBoxLayout()

        self.scroll_details.setWidget(self.widget_details)
        self.widget_details.setLayout(self.lay_details)

        self.right_part.addLayout(Wrapper(self.title_right_part))
        self.right_part.addLayout(Wrapper(self.title_app))

        self.right_part.setMinimumWidth(500)

        self.right_part.addElement(self.scroll_details)

        h_list.addWidget(self.right_part)

        self.main.addLayout(h_list)
        layout.addWidget(self.main)
        layout.addSpacing(-20)

        self.setLayout(layout)

        stats_signal.thread_upd_history.connect(self.setData)

    def on_text_changed(self, text):
        for widget in self.widget.findChildren(QWidget):
            if widget.objectName() in text or text == "":
                widget.show()
            else:
                widget.hide()

    def setData(self, history: list):
        self.model.setStringList([])
        self.clear_layout(self.lay)

        apps_completer = []

        for app_history in reversed(history):
            title = app_history[0]
            start = app_history[1]
            end = app_history[2]
            time = app_history[3]
            session_counts = app_history[4]

            self.history_card = HistoryCard(title=title, last_session=f"{start} - {end}", time=normal_time(time, "short"),
                                            session_count=session_counts)
            self.history_card.setObjectName(title)
            self.history_card.clicked.connect(self.setDetails)

            apps_completer.append(title)
            self.lay.addLayout(Wrapper(self.history_card))

        if len(apps_completer) == 0:
            self.setDetails("")
            self.label = QLabel()
            self.label.setText("Мы пока не нашли вашу историю")
            self.label.setPalette(self.palette_label)
            self.label.setFont(self.font_label)

            self.lay.addLayout(Wrapper(self.label))

        self.lay.addStretch()
        self.model.setStringList(apps_completer)

        self.widget.update()
        self.widget.repaint()

    def setDetails(self, title):
        self.clear_layout(self.lay_details)
        get_session = get_history_session(self.db_session, title)

        self.title_app.setText(title)
        self.mini_label_font = self.font_label
        self.mini_label_font.setPointSize(13)

        self.mini_palette = self.palette_label
        self.mini_palette.setColor(QPalette.ColorRole.Base, QColor("#b8d4af"))
        self.mini_palette.setColor(QPalette.ColorRole.Window, QColor("#b8d4af"))

        for session in get_session:
            seconds = session[0]
            time_session = f"{session[1]} - {session[2]}"

            self.detail_label = QLabel()
            self.detail_label.setPalette(self.mini_palette)
            self.detail_label.setText(f"{time_session}\n{normal_time(seconds, with_sec=True)}")
            self.detail_label.setFont(self.mini_label_font)

            self.lay_details.addWidget(self.detail_label)
            self.lay_details.addSpacing(25)

        self.lay_details.addStretch()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item is None:
                continue

            w = item.widget()
            l = item.layout()
            s = item.spacerItem()

            if w is not None:
                layout.removeWidget(w)
                w.setParent(None)
                w.deleteLater()
            elif l is not None:
                self.clear_layout(l)
                layout.removeItem(l)
            elif s is not None:
                layout.removeItem(s)

    def update_completer(self, name, completer, app_list):
        app_list.append(name)
        completer.update_items(app_list)