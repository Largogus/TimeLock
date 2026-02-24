from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtGui import QColor, QPalette
from Widgets.Buttons.Button import Button
from Widgets.CategoryCard import CategoryCard
from Widgets.Panels.SidePanel import SidePanel
from Widgets.Wrapper import Wrapper
from core.command.settings import get_settings
from core.db.session import SessionLocalCash, SessionLocal
from core.system.date import today, normal_time
from Widgets.Frame import BaseFrame
from Widgets.CircleProgressBar import CircleProgressBar
from core.signals.tracker_signals import signal
from core.thread.category.top_category import TopCategory
from core.system.config import FONT_FAMILY


class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.sidepanel = SidePanel(self)
        self.db_session = SessionLocal()
        self.db_session_cash = SessionLocalCash

        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(-20)
        self.date_frame = BaseFrame(QVBoxLayout())
        self.date_frame.mainLayout.setContentsMargins(20, 20, 20, 0)
        self.date_frame.setBorderRadius(0)

        font_font = self.font()
        font_font.setFamily(FONT_FAMILY)
        font_font.setPointSize(16)
        font_font.setBold(True)

        self.setFont(font_font)

        self.header = BaseFrame()
        self.header.setBackgroundColor(alpha=0)
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

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

        common_limit = get_settings(self.db_session, "total_limit_pc", int)
        if common_limit != 0:
            common_limit_str = f'Лимит: {normal_time(common_limit)}'
        else:
            common_limit_str = "Лимит не установлен"

        self.limit_label = QLabel(text=f"{common_limit_str}")
        self.limit_label.setMinimumWidth(125)
        limit_label_font = self.limit_label.font()
        limit_label_font.setPointSize(10)
        self.limit_label.setFont(limit_label_font)
        self.limit_label.setPalette(QColor(255, 255, 255))
        self.limit_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        wrapper = Wrapper(self.progress_bar)
        wrapper_to_limit_text = Wrapper(self.limit_label)

        self.date_frame.addLayout(wrapper)
        self.date_frame.addLayout(wrapper_to_limit_text)

        self.date_frame.addSpacer(spacer)

        signal.sessionUpdate.connect(lambda time: self.progress_bar.upd(time))

        self.category_label = QLabel()
        self.category_label.setText("Категории сегодня:")
        font = self.category_label.font()
        font.setPointSize(16)
        self.category_label.setFont(font)
        self.category_label.setPalette(QColor(255, 255, 255))

        wrapper_category_label = Wrapper(self.category_label)

        self.date_frame.addLayout(wrapper_category_label)
        self.date_frame.addSpacer(spacer)

        self.top_worker = TopCategory(self.db_session_cash, interval=10)
        self.top_worker.topUpdated.connect(self.update_top_categories)
        self.top_worker.start()

        self.h = QHBoxLayout()

        self.date_frame.addLayout(self.h)

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

    def update_top_categories(self, top4: dict):
        while self.h.count():
            widget = self.h.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        has_nonzero = any(t != 0 for t in top4.values())

        if not has_nonzero:
            top4 = {"Без категории": 0}

        for index, (category, total_time) in enumerate(sorted(top4.items(), key=lambda x: x[1], reverse=True)):
            if total_time != 0 or index == 0:
                category_card = CategoryCard(title=category, time=normal_time(total_time))
                category_card.setObjectName(category)
                category_card.clicked.connect(lambda checked, c=category_card: self.OpenSidePanel(c))
                self.h.addWidget(category_card)