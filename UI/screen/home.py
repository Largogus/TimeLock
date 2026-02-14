from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtGui import QColor, QFont, QPalette
from Widgets.Button import Button
from Widgets.CategoryCard import CategoryCard
from Widgets.Panels.SidePanel import SidePanel
from Widgets.Wrapper import Wrapper
from core.system.date import today, normal_time
from Widgets.Frame import BaseFrame
from Widgets.CircleProgressBar import CircleProgressBar
from core.signals.tracker_signals import signal


class Home(QWidget):
    def __init__(self):
        super().__init__()

        self.sidepanel = SidePanel(self)

        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(-20)
        self.date_frame = BaseFrame(QVBoxLayout())
        self.date_frame.mainLayout.setContentsMargins(20, 20, 20, 0)
        self.date_frame.setBorderRadius(0)

        self.font = QFont('Segoe UI', 16)
        self.font.setBold(True)

        self.setFont(self.font)

        self.header = BaseFrame()
        self.header.setBackgroundColor(alpha=0)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.header_frame = BaseFrame()

        self.date_label = QLabel()
        self.date_label.setMinimumWidth(180)
        self.date_label.setPalette(QPalette(QColor(255, 255, 255)))
        self.date_label.setText(f"Сегодня, {today()}")

        self.pause_limits = Button("Пауза лимитов", indicator=True, radius=6, alpha=[100, 120, 100], margin=4, ratio=64)

        self.header.addElement(self.date_label)
        self.header.mainLayout.addStretch(1)
        self.header.addElement(self.pause_limits)

        self.date_frame.addElement(self.header)

        spacer = QSpacerItem(0, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.date_frame.addSpacer(spacer)

        self.progress_bar = CircleProgressBar()

        self.limit_label = BaseFrame(text="Лимит не установлен")
        self.limit_label.setMinimumWidth(125)

        wrapper = Wrapper(self.progress_bar)
        wrapper_to_limit_text = Wrapper(self.limit_label)

        self.date_frame.addLayout(wrapper)
        self.date_frame.addLayout(wrapper_to_limit_text)

        self.date_frame.addSpacer(spacer)

        signal.sessionUpdate.connect(lambda time: self.progress_bar.upd(time))

        # self.CountTimePC = CountWindowsLife()
        # self.CountTimePC.tick.connect(lambda uptime: self.progress_bar.upd(uptime))
        # self.CountTimePC.start()

        self.category_label = QLabel()
        self.category_label.setText("Категории сегодня:")
        font = self.category_label.font()
        font.setPointSize(16)
        self.category_label.setFont(font)
        self.category_label.setPalette(QColor(255, 255, 255))

        wrapper_category_label = Wrapper(self.category_label)

        self.date_frame.addLayout(wrapper_category_label)
        self.date_frame.addSpacer(spacer)

        template = {"Работа": {"time": 57600, "name": ["Google Chrome", "Python"], "exe": ["chrome.exe", "python.exe"]},
                         "Мессенджеры": {"time": 21600, "name": ["Telegram"], "exe": ["telegram.exe"]},
                         "Игры": {"time": 14800, "name": ["Minecraft"], "exe": ["minecraft.exe"]},
                         "Музыка": {"time": 25200, "name": ["Spotify"], "exe": ["spotify.exe"]},
                         "Рисование": {"time": 0, "name": ["Paint"], "exe": "paint.exe"}}

        top4 = dict(sorted(template.items(), key=lambda x: x[1]['time'], reverse=True)[:4]) # ЗАМЕНИТЬ НА SQL

        h = QHBoxLayout()

        for index, (category, data) in enumerate(top4.items()):
            if data['time'] != 0 or index == 0:
                category_card = CategoryCard(title=category, time=normal_time(data['time']))
                category_card.setObjectName(category)
                category_card.clicked.connect(lambda checked, c=category_card: self.OpenSidePanel(c))
                h.addWidget(category_card)

        self.date_frame.addLayout(h)

        self.date_frame.mainLayout.addStretch(1)

        mainLayout.addWidget(self.date_frame)

        mainLayout.addSpacing(-20)

        self.setLayout(mainLayout)

        self.sidepanel.raise_()

    def resizeEvent(self, event):
        self.sidepanel.upd()

    def OpenSidePanel(self, card: CategoryCard):
        obj = card.objectName()

        if self.sidepanel._is_hide:
            self.sidepanel.setDate(obj)
        self.sidepanel.toggle()