from threading import Lock

from loguru import logger

from core.models.App import App
from core.models.AppSession import AppSession
from core.db.session import SessionLocal
from datetime import datetime


_last_focus_map = {}
_focus_lock = Lock()


def handle_session(app: App, db_session=None, focus: int = 0):
    from core.db.session import SessionLocal

    if app is None:
        return

    if db_session is None:
        with SessionLocal() as db_session_inner:
            _handle_session_logic(app, db_session_inner, focus)
    else:
        _handle_session_logic(app, db_session, focus)


def _handle_session_logic(app: App, db_session, focus: int):
    from core.models.AppSession import AppSession
    from datetime import datetime

    active_session = db_session.query(AppSession).filter_by(end_time=None).first()

    if active_session and active_session.app_id == app.id:
        return

    if active_session and active_session.app_id != app.id:
        active_session.end_time = datetime.now()

    if app.id == "close":
        return

    new_session = AppSession(
        app_id=app.id,
        start_time=datetime.now(),
        focus_mode=focus
    )
    db_session.add(new_session)
    try:
        db_session.flush()
    except Exception as e:
        db_session.rollback()
        logger.error(f"Ошибка при создании сессии: {e}")
        return