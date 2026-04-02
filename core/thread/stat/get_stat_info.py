from PySide6.QtCore import QThread
from core.statistic.history_stats import get_history
from core.signals.statistics_signsl import stats_signal
from core.signals.tracker_signals import signal


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