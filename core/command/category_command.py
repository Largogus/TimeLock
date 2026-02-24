from datetime import datetime, time, date
from loguru import logger
from core.models.App import App
from core.models.AppSession import AppSession
from core.models.CategoryLimit import CategoryLimit
from sqlalchemy import func, and_


def get_category(db_session) -> list:

    category = db_session.query(CategoryLimit).all()
    category = [x.category_name for x in category]

    return category


def set_category(db_session, name, limit: int = 0):
    try:
        settings = db_session.query(CategoryLimit).filter_by(category_name=name).first()

        if not settings:
            settings = CategoryLimit(category_name=name, limit_seconds=limit)
            db_session.add(settings)
        else:
            settings.limit_seconds = limit

        db_session.commit()
    except Exception as e:
        logger.critical(f"Критическая ошибка при занесении в базу данных: {e}")
        db_session.rollback()


def count_time_category(db_session, category):
    start_of_day = datetime.combine(datetime.today(), datetime.min.time())
    now = datetime.now()

    data = db_session.query(AppSession).join(App).filter(
        App.category == category,
        AppSession.start_time <= now,
        func.coalesce(AppSession.end_time, now) >= start_of_day
    )

    total_time = 0

    for s in data:
        real_start = max(s.start_time, start_of_day)
        real_end = min(s.end_time or now, now)

        seconds = int((real_end - real_start).total_seconds())

        if seconds <= 0:
            continue

        total_time += seconds

    return total_time


def count_limit_category(db_session, category):
    data = db_session.query(CategoryLimit).filter(CategoryLimit.category_name == category).first()

    return data.limit_seconds

