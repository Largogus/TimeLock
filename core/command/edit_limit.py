from sqlalchemy import func
from core.models.App import App
from core.models.AppLimit import AppLimit
from core.models.CategoryLimit import CategoryLimit
from PySide6.QtCore import QDateTime
from loguru import logger


def edit_limit_app(db_session, app, time):
    real_time = time

    if time == 0:
        real_time = None

    try:
        app_obj = db_session.query(App).filter_by(name=app).first()

        if not app_obj:
            return False

        if not app_obj.limit:
            app_obj.limit = AppLimit(
                daily_limit=real_time,
                enabled=True
            )
        else:
            app_obj.limit.daily_limit = real_time
            app_obj.limit.enabled = True

        db_session.commit()
        return True

    except Exception:
        db_session.rollback()
        logger.critical("Ошибка при изменении лимита")
        return False


def delete_limit_app(db_session, app):
    try:
        app_obj = db_session.query(App).filter_by(name=app).first()

        if not app_obj:
            return False

        else:
            app_obj.limit.daily_limit = None
            app_obj.limit.enabled = True

        db_session.commit()
        return True
    except Exception:
        db_session.rollback()
        logger.critical("Ошибка при удалении лимита")
        return False


def get_app_limit(db_session, app):
    app_obj = db_session.query(App).filter_by(name=app).first()
    print(app_obj.limit)

    if app_obj.limit is None:
        return False, 0

    return app_obj.limit.enabled, app_obj.limit.daily_limit


def turn_app_limit(db_session, app):
    try:
        app_obj = db_session.query(App).filter_by(name=app).first()

        if not app_obj:
            return False

        else:
            state, _ = get_category_limit(db_session, app)
            app_obj.limit.enabled = not bool(state)

        db_session.commit()
        return True

    except Exception:
        db_session.rollback()
        logger.critical("Ошибка при изменении лимита")
        return False


def edit_limit_category(db_session, category, time):
    real_time = time

    if time == 0:
        real_time = None

    try:
        app_obj = db_session.query(CategoryLimit).filter_by(category_name=category).first()

        if not app_obj:
            return False

        else:
            app_obj.limit_seconds = real_time

        db_session.commit()
        return True

    except Exception:
        db_session.rollback()
        logger.critical("Ошибка при изменении лимита")
        return False


def delete_limit_category(db_session, category):
    try:
        app_obj = db_session.query(CategoryLimit).filter_by(category_name=category).first()

        if not app_obj:
            return False
        else:
            app_obj.limit_seconds = None

        db_session.commit()
        return True
    except Exception:
        db_session.rollback()
        logger.critical("Ошибка при удалении лимита")
        return False


def get_category_limit(db_session, category):
    app_obj = db_session.query(CategoryLimit).filter_by(category_name=category).first()

    return app_obj.enabled, app_obj.limit_seconds


def turn_category_limit(db_session, category):
    try:
        app_obj = db_session.query(CategoryLimit).filter_by(category_name=category).first()

        if not app_obj:
            return False

        else:
            state, _ = get_category_limit(db_session, category)
            app_obj.enabled = not bool(state)

        db_session.commit()
        return True

    except Exception:
        db_session.rollback()
        logger.critical("Ошибка при изменении лимита")
        return False