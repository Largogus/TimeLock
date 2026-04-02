from datetime import date, datetime, time, timedelta
from PySide6.QtCore import QThread
from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

from core.db.db_writer import db_writer
from core.db.session import SessionLocal
from core.db.session_logic import handle_session
from core.models.AppSession import AppSession
from core.signals.core_events import core_events
from core.signals.edit_signals import signal_edit
from core.system.config import SETTINGS
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
        self._last_heartbeat = datetime.now()
        self._last_commit = datetime.now()
        self._interval = 1
        self.daily_cache = {}
        self.db_session_factory = db_session_factory

    def update_daily_time(self, daily_cache):
        with SessionLocal() as session:
            today = date.today()
            for app_id, data in daily_cache.items():
                record = session.query(DailyStat).filter_by(date=today, app_id=app_id).first()
                if record:
                    record.total_seconds = data['total_seconds']
                    record.sessions_count = data['sessions_count']
                    record.focus_seconds = data['focus_seconds']
                else:
                    session.add(DailyStat(
                        date=today,
                        app_id=app_id,
                        total_seconds=data['total_seconds'],
                        sessions_count=data['sessions_count'],
                        focus_seconds=data['focus_seconds']
                    ))
            session.commit()

    def load_initial_cache(self, db_session):
        today_start = datetime.combine(date.today(), time.min)
        now = datetime.now()
        sessions = db_session.query(AppSession).all()
        for session_obj in sessions:
            start = max(session_obj.start_time, today_start)
            end = session_obj.end_time or now
            total_seconds = int((end - start).total_seconds())
            focus_seconds = total_seconds if session_obj.focus_mode else 0
            app_id = session_obj.app_id
            if app_id not in self.daily_cache:
                self.daily_cache[app_id] = {"total_seconds": 0, "sessions_count": 0, "focus_seconds": 0}
            self.daily_cache[app_id]['total_seconds'] += total_seconds
            self.daily_cache[app_id]['sessions_count'] += 1
            self.daily_cache[app_id]['focus_seconds'] += focus_seconds

    @staticmethod
    def remove_session(*args, **kwargs):
        period = SETTINGS.get("keep_session", 1)
        threshold = datetime.combine(date.today(), time.min) if period == 1 else datetime.now() - timedelta(days=period)
        with SessionLocal() as session:
            try:
                result = session.execute(
                    AppSession.__table__.delete().where(AppSession.start_time < threshold)
                )
                session.commit()
                logger.success(f"Удалено {result.rowcount} старых сессий за {period} дней")
            except Exception as e:
                session.rollback()
                logger.error(f"Ошибка при удалении старых сессий: {e}")


    @staticmethod
    def remove_archive(*args, **kwargs):
        period = SETTINGS.get("keep_archive", 31)
        threshold = date.today() if period == 1 else (datetime.now() - timedelta(days=period)).date()
        with SessionLocal() as session:
            try:
                result = session.execute(
                    DailyStat.__table__.delete().where(DailyStat.date < threshold)
                )
                session.commit()
                logger.success(f"Удалено {result.rowcount} старых архивных записей за {period} дней")
            except Exception as e:
                session.rollback()
                logger.error(f"Ошибка при удалении архивных записей: {e}")

    @staticmethod
    def fix_unclosed_sessions(*args, **kwargs):
        now = datetime.now()
        with SessionLocal() as session:
            open_sessions = session.query(AppSession).filter(AppSession.end_time.is_(None)).all()
            for s in open_sessions:
                last_active = s.start_time or now
                delta = (now - last_active).total_seconds()
                if delta > 60:
                    s.end_time = last_active
                    logger.info(f"Закрыта сессия до сна ({(last_active - s.start_time).total_seconds():.0f} сек)")
                else:
                    s.end_time = now
            session.commit()

    def run(self):
        db_session = self.db_session_factory()
        try:
            self.load_initial_cache(db_session)

            db_writer.submit(self.remove_session)

            db_writer.submit(self.remove_archive)

            db_writer.submit(self.fix_unclosed_sessions)

            db_writer.submit(lambda session: self.update_daily_time(self.daily_cache.copy()))

            signal.sessionUpdate.emit(get_total_pc_time_today())

            while not self.isInterruptionRequested():
                try:
                    today = date.today()
                    now = datetime.now()

                    if today != self._current_date:
                        signal_edit.upd_limit.emit()
                        self._current_date = today
                        self.daily_cache = {}
                        db_writer.submit(lambda session: self.update_daily_time(self.daily_cache.copy()))
                        db_writer.submit(self.remove_session)
                        db_writer.submit(self.remove_archive)
                        db_writer.submit(self.fix_unclosed_sessions)
                        self.load_initial_cache(db_session)

                    app, hwnd, active_app_name, active_app_path = tracker_tick(db_session)

                    real_delta = (now - self._last_heartbeat).total_seconds()
                    if real_delta > 45:
                        db_writer.submit(self.fix_unclosed_sessions)
                        self._current_app_id = None

                    if app:
                        app_id = app.id
                        if app_id not in self.daily_cache:
                            self.daily_cache[app_id] = {"total_seconds": 0, "sessions_count": 0, "focus_seconds": 0}

                        if self._current_app_id != app_id:
                            if self._current_app_id is not None:
                                self.daily_cache[self._current_app_id]['sessions_count'] += 1
                            self._current_app_id = app_id

                        db_writer.submit(
                            lambda session: handle_session(app, db_session=session, focus=SETTINGS.get("focus", 0)))

                        if not SETTINGS.get("focus", 0):
                            self.daily_cache[app_id]['total_seconds'] += self._interval
                        else:
                            self.daily_cache[app_id]['focus_seconds'] += self._interval

                        self._last_heartbeat = now
                    else:
                        if self._current_app_id is not None:
                            db_writer.submit(lambda session: handle_session(App(id="close"), db_session=session,
                                                                            focus=SETTINGS.get("focus", 0)))

                        self._current_app_id = None
                        self._last_heartbeat = now

                    if (now - self._last_commit).total_seconds() >= 60:
                        db_writer.submit(lambda session: self.update_daily_time(self.daily_cache.copy()))
                        self._last_commit = now

                    signal.sessionUpdate.emit(get_total_pc_time_today())

                except Exception as e:
                    signal.errorOccurred.emit(str(e))
                    db_session.rollback()
                    self._interval = 1

                for _ in range(self._interval):
                    if self.isInterruptionRequested():
                        break
                    QThread.sleep(1)

        finally:
            db_writer.submit(self.update_daily_time, self.daily_cache.copy())
            db_session.close()

    def stop(self):
        self.requestInterruption()
        self.wait()