from PySide6.QtCore import QThread, Signal
from core.system.config import SETTINGS
from core.thread.table.get_time_application import get_time_application
from loguru import logger


class TableDataLoader(QThread):
    statsReady = Signal(list)

    def __init__(self, db_session_factory):
        super().__init__()

        self.db_session_factory = db_session_factory

    def run(self):
        db_session = self.db_session_factory()

        try:
            interval = SETTINGS.get("tracking_interval_seconds", 1)

            while not self.isInterruptionRequested():
                try:
                    data = get_time_application(db_session)
                    self.statsReady.emit(data)

                except Exception as e:
                    logger.critical(f"Поток умер, причина: {e}")
                    db_session.rollback()

                for _ in range(interval):
                    if self.isInterruptionRequested():
                        break
                    QThread.sleep(1)

        finally:
            db_session.close()

    def stop(self):
        self.requestInterruption()
        self.wait()