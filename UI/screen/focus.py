from PySide6.QtCore import QTime, QDateTime
from PySide6.QtGui import QColor, QPalette, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTimeEdit
from Widgets.Buttons.Button import Button
from Widgets.Frame import BaseFrame
from Widgets.Line import Line
from Widgets.Modal.FocusAllowedModal import FocusAllowedModal
from Widgets.ProgressBar.FocusProgressBar import FocusProgressBar
from Widgets.Timer import Timer
from Widgets.Wrapper import Wrapper
from core.command.settings import set_settings
from core.db.session import SessionLocal
from core.signals.notification_signals import show_notification
from core.system.config import SETTINGS
from core.system.date import time_for_qt


class Focus(QWidget):
    def __init__(self):
        super().__init__()

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
        title.setText('Фокус')

        info_window = QLabel()
        info_window.setText("Режим концентрации")
        info_window.setPalette(QPalette(QColor(163, 163, 163)))
        info_window_font = info_window.font()
        info_window_font.setPointSize(14)
        info_window.setFont(info_window_font)

        self.main.addElement(title)
        self.main.addElement(info_window)

        self.main.addElement(Line('H'))

        self.focus_progress_bar = FocusProgressBar(100000)
        self.focus_progress_bar.updateRemainingTime(100000)

        self.main.addLayout(Wrapper(self.focus_progress_bar))

        self.timer = QTimeEdit()
        self.timer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer.setButtonSymbols(QTimeEdit.ButtonSymbols.NoButtons)
        self.timer.setMinimumWidth(250)
        self.timer.setMinimumHeight(50)

        timer_font = self.timer.font()
        timer_font.setPointSize(14)
        timer_font.setBold(True)

        self.timer.setFont(timer_font)

        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Base, QColor("#F2F4F6"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#111827"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#27AE60"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
        self.timer.setPalette(palette)

        self.main.addLayout(Wrapper(self.timer))

        self.focus_allowed = Button(name="Разрешённые приложения", align=Qt.AlignmentFlag.AlignCenter, radius=8)
        self.focus_allowed.setMinimumWidth(400)
        self.focus_allowed.setBackgroundColor(QColor("#8fefae"))
        self.focus_allowed.setBackgroundHover(QColor("#7eeda1"))
        self.focus_allowed.setBackgroundPressed(QColor("#baf8cd"))

        self.focus_allowed.clicked.connect(lambda: FocusAllowedModal().show())

        self.main.mainLayout.addSpacing(30)

        self.focus_start = Button(name="Включить фокус", align=Qt.AlignmentFlag.AlignCenter, radius=8)
        self.focus_start.setMinimumWidth(400)
        self.focus_start.setBackgroundColor(QColor("#66f092"))
        self.focus_start.setBackgroundHover(QColor("#4dfe85"))
        self.focus_start.setBackgroundPressed(QColor("#67fe97"))
        self.focus_start.clicked.connect(self.startTimerThread)

        self.main.addLayout(Wrapper(self.focus_allowed))

        self.main.mainLayout.addSpacing(8)

        self.main.addLayout(Wrapper(self.focus_start))

        self.main.mainLayout.addStretch()

        layout.addWidget(self.main)
        layout.addSpacing(-20)
        self.setLayout(layout)

        self.time = Timer()
        self.time.stopped.connect(self.reload)
        self.time.timeout.connect(self.updTime)

    def startTimerThread(self):
        focus_state = SETTINGS.get("focus", 0)

        if self.timer.time() == QTime(0, 0) and not focus_state:
            self.focus_progress_bar.updateRemainingTime(100000)
            return

        if focus_state:
            self.time.stop()
        else:
            show_notification.show_notification_focus_on.emit()
            self.focus_start.setText("Выключить фокус")
            self.focus_start.setBackgroundColor(QColor("#ef706b"))
            self.focus_start.setBackgroundHover(QColor("#f0918e"))
            self.focus_start.setBackgroundPressed(QColor("#f16a65"))

            self.timer.setEnabled(False)

            time = self.timer.time()

            self.total_seconds = QTime(0, 0).secsTo(time)

            self.end_time = QDateTime.currentDateTime().addSecs(self.total_seconds)

            self.focus_progress_bar.setTotalTime(self.total_seconds)

            self.time.start(1000)

        with SessionLocal() as session:
            set_settings(session, 'focus', int(not focus_state), int)

    def updTime(self):
        remaining = QDateTime.currentDateTime().secsTo(self.end_time)

        if remaining <= 0:
            with SessionLocal() as session:
                set_settings(session, 'focus', 0, int)
            show_notification.show_notification_focus_off.emit()
            self.time.stop()
        else:
            self.focus_progress_bar.updateRemainingTime(remaining)
            self.timer.setTime(time_for_qt(remaining))

    def reload(self):
        self.focus_start.setText("Включить фокус")
        self.focus_start.setBackgroundColor(QColor("#66f092"))
        self.focus_start.setBackgroundHover(QColor("#4dfe85"))
        self.focus_start.setBackgroundPressed(QColor("#67fe97"))

        self.timer.setEnabled(True)
        self.focus_progress_bar.updateRemainingTime(100000)

