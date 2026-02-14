from PySide6.QtCore import QThread, Signal
from core.command.settings import get_settings
from core.db.session_logic import close_session
from core.db.session import SessionLocal
from core.thread.main.tracker_tick import tracker_tick
from core.signals.tracker_signals import signal
from core.system.get_total_pc_time_today import get_total_pc_time_today


class TrackerThread(QThread):
    def __init__(self, db_session_factory):
        super().__init__()

        self.db_session_factory = db_session_factory

    def run(self):
        db_session = self.db_session_factory()

        while not self.isInterruptionRequested():
            try:
                active_app_name = tracker_tick(db_session)
                if active_app_name:
                    res_time = get_total_pc_time_today(db_session)
                    signal.sessionUpdate.emit(res_time)

                interval = get_settings(
                    db_session,
                    "tracking_interval_seconds",
                    cast_type=int)

            except Exception as e:
                signal.errorOccurred.emit(str(e))
                db_session.rollback()
                interval = 1

            finally:
                db_session.close()

            for _ in range(interval):
                if self.isInterruptionRequested():
                    break
                QThread.sleep(1)

    def stop(self):
        self.requestInterruption()

        db_session = self.db_session_factory()
        try:
            close_session(db_session)
        finally:
            db_session.close()

        close_session(SessionLocal())
        self.wait()