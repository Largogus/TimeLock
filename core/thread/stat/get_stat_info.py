from datetime import date, datetime, time
from PySide6.QtCore import QThread
from sqlalchemy import func, delete
from sqlalchemy.exc import SQLAlchemyError
from core.command.settings import get_settings
from core.db.session_logic import close_session
from core.db.session import SessionLocal
from core.models.AppSession import AppSession
from core.signals.edit_signals import signal_edit
from core.statistic.get_all_stat import get_all_stats
from core.statistic.get_bar_chart_data import get_category_info, get_app_info
from core.statistic.history_stats import get_history
from core.thread.main.tracker_tick import tracker_tick
from core.signals.statistics_signsl import stats_signal
from core.signals.tracker_signals import signal
from core.system.get_total_pc_time_today import get_total_pc_time_today
from core.models.App import App
from core.models.DailyStat import DailyStat
from loguru import logger


class StatisticThread(QThread):
    def __init__(self, db_session_factory):
        super().__init__()

        self._interval = 1
        self.db_session_factory = db_session_factory
        self.period = "День"

        stats_signal.click_period.connect(self.setPeriod)

    def run(self):
        db_session = self.db_session_factory()
        self.first = True

        while not self.isInterruptionRequested():
            try:
                history = get_history(db_session)
                stats_signal.thread_upd_history.emit(history)

            except Exception as e:
                signal.errorOccurred.emit(str(e))
                db_session.rollback()

            finally:
                db_session.close()

            if self.first:
                self.first = False
            else:
                for _ in range(20):
                    if self.isInterruptionRequested():
                        break
                    QThread.sleep(1)

    def setPeriod(self, period):
        self.period = period