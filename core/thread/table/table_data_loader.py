from PySide6.QtCore import QThread, Signal
from core.command.settings import get_settings
from core.thread.table.get_time_application import get_time_application
from loguru import logger


class TableDataLoader(QThread):
    statsReady = Signal(list)

    def __init__(self, db_session_factory):
        super().__init__()

        self.db_session_factory = db_session_factory

    def run(self):
        while not self.isInterruptionRequested():
            db_session = self.db_session_factory()
            interval = get_settings(
                    db_session,
                    "tracking_interval_seconds",
                    cast_type=int)

            try:
                data = get_time_application(db_session)

                self.statsReady.emit(data)
            except Exception as e:
                logger.critical(f"Поток умер, причина: {e}")
            finally:
                db_session.close()

            for _ in range(interval):
                if self.isInterruptionRequested():
                    break
                QThread.sleep(1)

    def stop(self):
        self.requestInterruption()
        self.wait()