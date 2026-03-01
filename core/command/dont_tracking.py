from core.models.App import App
from loguru import logger


def dont_tracking(db_session, app_id):
    try:
        app = (db_session.query(App)
            .filter(App.id == app_id)
            .first()
        )

        if not app:
            return False

        app.status = "ignored"

        db_session.commit()
        return True

    except Exception:
        db_session.rollback()
        logger.critical("Изменение не удалось")
        return False