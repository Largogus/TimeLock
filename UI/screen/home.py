from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtCore import Qt
from Widgets.Button import Button
from Widgets.CategoryCard import CategoryCard
from Widgets.Wrapper import Wrapper
from core.system.date import today
from Widgets.Frame import BaseFrame
from Widgets.CircleProgressBar import CircleProgressBar
from core.thread.time.window_time_counter import CountWindowsLife
# from core.signals.signal import SignalObject


class Home(QWidget):
    def __init__(self):
        super().__init__()

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
        self.limit_label.setFontFrame('Segoe UI', 12)
        self.limit_label.setMinimumWidth(125)

        wrapper = Wrapper(self.progress_bar)
        wrapper_to_limit_text = Wrapper(self.limit_label)

        self.date_frame.addLayout(wrapper)
        self.date_frame.addLayout(wrapper_to_limit_text)

        self.date_frame.addSpacer(spacer)

        self.CountTimePC = CountWindowsLife()
        self.CountTimePC.tick.connect(lambda uptime: self.progress_bar.upd(uptime))
        self.CountTimePC.start()

        self.category_label = QLabel()
        self.category_label.setText("Категории сегодня")
        self.category_label.setFont(QFont("Segoe UI", 16))
        self.category_label.setPalette(QColor(255, 255, 255))

        wrapper_category_label = Wrapper(self.category_label)

        self.date_frame.addLayout(wrapper_category_label)
        self.date_frame.addSpacer(spacer)

        self.template = {"chrome.exe": {"time": 25200, "name": "Google Chrome", "category": "Работа"},
                         "telegram.exe": {"time": 21600, "name": "Telegram", "category": "Мессенджер"},
                         "minecraft.exe": {"time": 14400, "name": "Minecraft", "category": "Игры"},
                         "python.exe": {"time": 32400, "name": "Google Chrome", "category": "Работа"},
                         "spotify.exe": {"time": 25200, "name": "Google Chrome", "category": "Музыка"}}

        h = QHBoxLayout()

        self.category_card = CategoryCard()
        self.category_card1 = CategoryCard()
        self.category_card2 = CategoryCard()
        self.category_card3 = CategoryCard()

        h.addWidget(self.category_card)
        h.addWidget(self.category_card1)
        h.addWidget(self.category_card2)
        h.addWidget(self.category_card3)

        self.date_frame.addLayout(h)

        self.date_frame.mainLayout.addStretch(1)

        mainLayout.addWidget(self.date_frame)

        mainLayout.addSpacing(-20)

        self.setLayout(mainLayout)