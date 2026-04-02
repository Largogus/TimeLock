from loguru import logger

from core.db.session import SessionLocal
from core.models.FocusAllowed import FocusAllowed
from core.models.App import App


def is_focus_allowed(session):
    try:
        allowed_apps = session.query(FocusAllowed).join(App).filter(App.status == "tracking").all()
        return [fa.app_id for fa in allowed_apps]
    except Exception as e:
        logger.exception(f"Ошибка при получении списка разрешенных Фокус-приложений: {e}")
        return []


def set_focus_allowed(session, app_id):
    try:
        fa = session.query(FocusAllowed).filter(FocusAllowed.app_id == app_id).first()
        if not fa:
            session.add(FocusAllowed(app_id=app_id))
            logger.info(f"Фокус разрешен для приложения {app_id}")
        else:
            session.delete(fa)
            logger.info(f"Фокус запрещен для приложения {app_id}")
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(f"Ошибка при смене разрешения Фокуса для {app_id}: {e}")