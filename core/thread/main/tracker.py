from datetime import date, datetime, time
from PySide6.QtCore import QThread
from sqlalchemy import func, delete
from sqlalchemy.exc import SQLAlchemyError
from core.command.settings import get_settings
from core.db.session_logic import close_session
from core.db.session import SessionLocal
from core.models.AppSession import AppSession
from core.signals.edit_signals import signal_edit
from core.thread.main.tracker_tick import tracker_tick
from core.signals.tracker_signals import signal
from core.system.get_total_pc_time_today import get_total_pc_time_today
from core.models.App import App
from core.models.DailyStat import DailyStat
from loguru import logger


class TrackerThread(QThread):
    def __init__(self, db_session_factory):
        super().__init__()

        self._current_app_id = None
        self._current_date = date.today()
        self._last_commit = datetime.now()
        self._daily_seconds = 0
        self._interval = 1

        self.daily_cache = {}

        self.db_session_factory = db_session_factory

    def update_daily_time(self, db_session):
        today = date.today()

        for app_id, data in self.daily_cache.items():
            record = db_session.query(DailyStat).filter_by(date=today, app_id=app_id).first()

            if record:
                record.total_seconds = data['total_seconds']
                record.sessions_count = data['sessions_count']
            else:
                new_record = DailyStat(
                    date=today,
                    app_id=app_id,
                    total_seconds=data['total_seconds'],
                    sessions_count=data['sessions_count']
                )
                db_session.add(new_record)

        db_session.commit()

    def load_initial_cache(self, db_session):
        today_start = datetime.combine(date.today(), time.min)
        now = datetime.now()

        total_time_subquery = (
            db_session.query(
                AppSession.app_id.label("app_id"),
                func.sum(
                    func.strftime('%s', func.min(func.coalesce(AppSession.end_time, now), now)) -
                    func.strftime('%s', func.max(AppSession.start_time, today_start))
                ).label("total_seconds"),
                func.count(AppSession.id).label("sessions_count")
            )
            .filter(
                AppSession.start_time < now,
                func.coalesce(AppSession.end_time, now) > today_start
            )
            .group_by(AppSession.app_id)
            .subquery()
        )

        query = (
            db_session.query(
                App,
                func.coalesce(total_time_subquery.c.total_seconds, 0),
                func.coalesce(total_time_subquery.c.sessions_count, 0)
            )
            .outerjoin(total_time_subquery, App.id == total_time_subquery.c.app_id)
            .filter(App.status == "tracking")
        )

        for app, total_seconds, sessions_count in query:
            self.daily_cache[app.id] = {
                "total_seconds": total_seconds,
                "sessions_count": sessions_count
            }

    def remove_session(self, db_session):
        today_start = datetime.combine(date.today(), time.min)

        try:
            session = (
                delete(AppSession)
                .where(AppSession.start_time < today_start)
            )
            result = db_session.execute(session)
            db_session.commit()

            deleted_count = result.rowcount
            logger.success(f"Успешно удалено {deleted_count} сессий")
        except SQLAlchemyError as e:
            db_session.rollback()
            logger.error(f"Не удалось очистить AppSession: {e}")

    def run(self):
        db_session = self.db_session_factory()
        try:
            self._interval = get_settings(
                db_session,
                "tracking_interval_seconds",
                cast_type=int
            ) or 1

            self.remove_session(db_session)
            self.load_initial_cache(db_session)

            while not self.isInterruptionRequested():
                try:
                    today = date.today()
                    if today != self._current_date:
                        signal_edit.upd_limit.emit()
                        self.update_daily_time(db_session)
                        self.remove_session(db_session)
                        self._current_date = today
                        self.load_initial_cache(db_session)

                    res = tracker_tick(db_session)

                    if res is not None:
                        active_app_name, active_app_path = res
                    else:
                        active_app_name, active_app_path = None, None

                    if active_app_name:
                        app = db_session.query(App).filter_by(name=active_app_name).first()
                        if app is None:
                            app = db_session.query(App).filter_by(path=active_app_path).first()
                        if app:
                            app_id = app.id

                            if app_id not in self.daily_cache:
                                self.daily_cache[app_id] = {"total_seconds": 0, "sessions_count": 0}

                            if self._current_app_id != app_id:
                                if self._current_app_id is not None:
                                    self.daily_cache[self._current_app_id]['sessions_count'] += 1
                                self._current_app_id = app_id

                            self.daily_cache[app_id]['total_seconds'] += self._interval

                        now = datetime.now()
                        if (now - self._last_commit).total_seconds() >= 60:
                            self.update_daily_time(db_session)
                            self._last_commit = now

                        res_time = get_total_pc_time_today(db_session)
                        signal.sessionUpdate.emit(res_time)

                except Exception as e:
                    signal.errorOccurred.emit(str(e))
                    db_session.rollback()
                    self._interval = 1

                for _ in range(self._interval):
                    if self.isInterruptionRequested():
                        break
                    QThread.sleep(1)

        finally:
            self.update_daily_time(db_session)
            db_session.close()

    def stop(self):
        self.requestInterruption()

        db_session = self.db_session_factory()
        try:
            close_session(db_session)
        finally:
            db_session.close()

        close_session(SessionLocal())
        self.wait()