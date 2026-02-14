from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt
from Widgets.Panels.PanelTemplate import PanelTemplate
from core.system.date import normal_time, plural
from Widgets.Button import Button
from Widgets.Wrapper import Wrapper
from core.system.config import FONT_FAMILY

template = {"Работа": {"time": 58500, "name": {"Google Chrome": 25010, "Python": 25000, "Microsoft Word": 1490, "PyCharm": 7000}, "exe": ["chrome.exe", "python.exe", "mw.exe", "pycahrm.exe"], "limit": 0}, # ТЕСТ
            "Мессенджеры": {"time": 3500, "name": {"Telegram": 3000, "MAX": 500}, "exe": ["telegram.exe", "max.exe"], "limit": 15425},
            "Игры": {"time": 14800, "name": ["Minecraft"], "exe": ["minecraft.exe"], "limit": 14800},
            "Музыка": {"time": 25200, "name": ["Google Chrome"], "exe": ["spotify.exe"], "limit": 19540},
            "Рисование": {"time": 0, "name": ["Paint"], "exe": "paint.exe"}, "limit": 0}


class SidePanel(PanelTemplate):
    def __init__(self, parent=None):
        super().__init__(parent, width=400)

        self.layout = QVBoxLayout()

        self.header = QHBoxLayout()

        self.name = QLabel()
        self.more = None

        self.application = {}

        wrapper_name = Wrapper(self.name)
        self.header.addLayout(wrapper_name)
        self.header.addWidget(self.close_btn)

        self.time_today = QLabel()

        self.wrapper_today = Wrapper(self.time_today)

        self.limit = Button(name="", radius=10, alpha=[100, 100, 100], font_color=Qt.GlobalColor.white, min=300, align=Qt.AlignmentFlag.AlignCenter)
        self.limit.setBackgroundColor(QColor('#0F1F17'))

        self.wrapper_limit = Wrapper(self.limit)

        # self.search = TextEdit(placeholder="Найти приложение…", border_radius=10, background=QColor('#0F1F17'))
        # self.search.setMaximumSize(350, 50)
        #
        # wrapper_search = Wrapper(self.search)

        self.top_app = QHBoxLayout()
        self.dop = QVBoxLayout()

        self.to_app = Button(name="Открыть все приложения →", radius=10, alpha=[100, 100, 100], font_color=Qt.GlobalColor.white, min=300, align=Qt.AlignmentFlag.AlignCenter)
        self.to_app.setBackgroundColor(QColor('#0F1F17'))

        self.wrapper_to_app = Wrapper(self.to_app)

        self.setLayout(self.layout)

    def setDate(self, obj):
        self.reload()

        self.name.setText(obj)
        date = template[obj]
        text = f"Сегодня: {normal_time(date['time'], format='short')} / Лимит: —" if date['limit'] == 0 else \
            f"Сегодня: {normal_time(date['time'], format='short')} / Лимит: {normal_time(date['limit'], format='short')}"
        self.time_today.setText(text)
        top_app = dict(sorted(date["name"].items(), key=lambda x: x[1], reverse=True)) # ЗАМЕНИТЬ НА SQL

        if date['limit']:
            self.limit.setText("Изменить лимит на категорию")
        else:
            self.limit.setText("Установить лимит на категорию")

        if len(top_app) > 3:
            lens = len(top_app) - 3
            top_3app = dict(sorted(date["name"].items(), key=lambda x: x[1], reverse=True)[:3])
            self.application = top_3app
            self.more = Button(f"+ ещё {lens} {plural(lens, ('приложение', 'приложения', 'приложений'))}", alpha=[0, 0, 0], font_color=Qt.GlobalColor.white, align=Qt.AlignmentFlag.AlignCenter)
            self.dop.addWidget(self.more)
        else:
            self.application = top_app

        self.run()

        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item is not None:
                self.layout.removeItem(item)

        self.layout.addLayout(self.header)
        self.layout.addLayout(self.wrapper_today)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.wrapper_limit)
        self.layout.addSpacing(20)
        self.layout.addLayout(self.top_app)

        if self.dop.count() > 0:
            self.layout.addSpacing(-10)
            self.layout.addLayout(self.dop)
        else:
            self.layout.addSpacing(15)

        self.layout.addLayout(self.wrapper_to_app)
        self.layout.addStretch(1)

    def run(self):  # Под SQL переделать!!!
        box1 = QVBoxLayout()
        box2 = QVBoxLayout()
        box3 = QVBoxLayout()

        font = QFont(FONT_FAMILY, 12)

        for k, t in self.application.items():
            name = QLabel(f"▷ {k}")
            name.setToolTip(k)
            name.setFont(font)
            time = QLabel(f"{normal_time(t, format='short')}")
            time.setFont(font)
            limit = QLabel(f"Нет")
            limit.setFont(font)

            box1.addWidget(name)
            box2.addWidget(time)
            box3.addWidget(limit)

        self.top_app.addLayout(box1)
        self.top_app.addSpacing(30)
        self.top_app.addLayout(box2)
        self.top_app.addSpacing(30)
        self.top_app.addLayout(box3)

        return

    def reload(self):
        self.clear_layout(self.top_app)
        self.clear_layout(self.dop)
        self.more = None

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