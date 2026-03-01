from datetime import datetime, time, date
from loguru import logger
from core.models.App import App
from core.models.AppLimit import AppLimit
from core.models.AppSession import AppSession
from core.models.CategoryLimit import CategoryLimit
from sqlalchemy import func, and_


def get_all_app(db_session, is_id: bool = False):
    session = db_session.query(App).filter(App.status == "tracking").all()

    if not is_id:
        list_session = [app.name for app in session]
    else:
        list_session = [(app.name, app.id) for app in session]

    return list_session


def get_all_app_with_category(db_session, category, is_id: bool = False):
    session = db_session.query(App).filter(and_(App.status == "tracking", App.category == category)).all()

    if not is_id:
        list_session = [app.name for app in session]
    else:
        list_session = [(app.name, app.id) for app in session]

    return list_session


def count_time_app_name(db_session, app_name):
    start_of_day = datetime.combine(datetime.today(), datetime.min.time())
    now = datetime.now()

    data = db_session.query(AppSession).join(App).filter(
        App.name == app_name,
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


def count_limit_app_name(db_session, app_name):
    data = (
        db_session.query(AppLimit)
        .join(App)
        .filter(App.name == app_name)
        .first()
    )

    return data.daily_limit if data else None