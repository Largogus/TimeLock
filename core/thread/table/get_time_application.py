from datetime import datetime, date, time
from sqlalchemy import func

from core.command.block_app import is_blocked
from core.models.App import App
from core.models.AppSession import AppSession
from core.models.CategoryLimit import CategoryLimit
from core.models.AppLimit import AppLimit
from core.system.date import normal_time


def get_time_application(session):
    today_start = datetime.combine(date.today(), time.min)
    now = datetime.now()

    total_time_subquery = (
        session.query(
            AppSession.app_id.label("app_id"),
            func.sum(
                func.strftime(
                    '%s',
                    func.min(func.coalesce(AppSession.end_time, now), now)
                ) -
                func.strftime(
                    '%s',
                    func.max(AppSession.start_time, today_start)
                )
            ).label("total_seconds")
        )
        .filter(
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start,
        )
        .group_by(AppSession.app_id)
        .subquery()
    )

    query = (
        session.query(
            App,
            AppLimit,
            func.coalesce(total_time_subquery.c.total_seconds, 0)
        )
        .select_from(App)
        .outerjoin(AppLimit, App.id == AppLimit.app_id)
        .outerjoin(total_time_subquery, App.id == total_time_subquery.c.app_id)
        .filter(App.status == "tracking")
    )

    category_query = (session.query(
        CategoryLimit.category_name,
        CategoryLimit.limit_seconds
        )
        .filter(CategoryLimit.enabled)
        .all()
    )

    category_dict = dict(category_query)

    apps_data = []

    for app, app_limit, total_seconds in query.all():
        total_seconds = int(total_seconds or 0)

        app_limit_value = app_limit.daily_limit if app_limit and app_limit.enabled else 0
        cat_limit = category_dict.get(app.category) or 0

        limit = app_limit_value or cat_limit or 0

        apps_data.append({
            "id": app.id,
            "name": app.name,
            "category": app.category,
            "today_time": normal_time(total_seconds, "short"),
            "limit": limit,
            "status": check_status(session, app, limit, total_seconds),
            "state": app.status
        })

    return apps_data


def check_status(db_session, app, limit, total_sec):
    if is_blocked(app, db_session):
        return False

    status = total_sec < limit if limit else True

    return status