from core.db.session import SessionLocal
from core.models.App import App
from loguru import logger
from core.signals.table_signals import signal


def changeCategory(app_name, new_cat):
    db_session = SessionLocal()

    try:
        app = db_session.query(App).filter(App.name == app_name).first()

        app.category = new_cat

        db_session.commit()

        signal.objectCategoryChanged.emit(app_name, new_cat)
    except Exception as e:
        logger.critical(f"Ошибка при изменении категории: {e}")
        db_session.rollback()
    finally:
        db_session.close()