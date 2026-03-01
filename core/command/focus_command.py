from datetime import datetime, time, date
from loguru import logger
from core.models.FocusAllowed import FocusAllowed
from core.models.App import App
from core.models.AppLimit import AppLimit
from core.models.AppSession import AppSession
from core.models.CategoryLimit import CategoryLimit
from sqlalchemy import func, and_


def is_focus_allowed(db_session):
    session = db_session.query(FocusAllowed).join(App).filter(App.status == "tracking").all()

    list_session = [app.app_id for app in session]

    return list_session


def set_focus_allowed(db_session, app_id):
    try:
        session = db_session.query(FocusAllowed).filter(FocusAllowed.app_id == app_id).first()

        if not session:
            data = FocusAllowed(app_id=app_id)

            db_session.add(data)

            db_session.commit()
            return

        db_session.delete(session)
        db_session.commit()
    except Exception:
        db_session.rollback()
        logger.error("Ошибка при смене разрешения Фокуса")