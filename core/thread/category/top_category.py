from PySide6.QtCore import QThread, Signal
from sqlalchemy import desc, func
from datetime import datetime, date, time
from core.models.App import App
from core.models.AppSession import AppSession
from loguru import logger


class TopCategory(QThread):
    topUpdated = Signal(dict)

    def __init__(self, db_session_factory, interval=30):
        super().__init__()
        self.interval = interval
        self.db_session_factory = db_session_factory

    def run(self):
        db_session = self.db_session_factory()
        try:
            while not self.isInterruptionRequested():
                try:
                    db_session.expire_all()

                    now = datetime.now()
                    today_start = datetime.combine(date.today(), time.min)

                    sessions = (
                        db_session.query(AppSession)
                        .join(App)
                        .filter(
                            AppSession.start_time < now,
                            func.coalesce(AppSession.end_time, now) > today_start,
                            App.status == "tracking"
                        )
                        .all()
                    )

                    total_seconds = 0

                    top_categories = {}

                    for session in sessions:
                        real_start = max(session.start_time, today_start)
                        real_end = min(session.end_time or now, now)

                        seconds = int((real_end - real_start).total_seconds())

                        if seconds > 0:
                            total_seconds += seconds

                            category = session.app.category or "Без категории"

                            top_categories[category] = int(top_categories.get(category, 0) + seconds)

                    top_categories = dict(
                        sorted(top_categories.items(), key=lambda x: x[1], reverse=True)[:4]
                    )

                    self.topUpdated.emit(top_categories)

                except Exception as e:
                    logger.error(f"Ошибка подсчёта топ-категорий: {e}")
                    self.topUpdated.emit({})

                for _ in range(self.interval):
                    if self.isInterruptionRequested():
                        break
                    QThread.sleep(1)

        finally:
            db_session.close()

    def stop(self):
        self.requestInterruption()
        self.wait()