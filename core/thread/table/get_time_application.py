from datetime import datetime, date, time
from core.models.models import App, AppSession, AppLimit
from core.system.date import normal_time


def get_time_application(session):
    today_start = datetime.combine(date.today(), time.min)
    today_end = datetime.combine(date.today(), time.max)

    apps = session.query(App, AppLimit).outerjoin(AppLimit, App.id == AppLimit.app_id).all()
    apps_data = []

    for app, app_limit in apps:
        limit = app_limit.daily_limit_minutes if app_limit else 0

        sessions = session.query(AppSession).filter(
            AppSession.app_id == app.id,
            AppSession.start_time >= today_start
        ).all()

        total_seconds = 0
        for s in sessions:
            start = s.start_time
            end = s.end_time or datetime.now()
            if end > today_end:
                end = today_end
            if start < today_start:
                start = today_start
            diff = (end - start).total_seconds()
            if diff > 0:
                total_seconds += diff

        apps_data.append({
            "id": app.id,
            "name": app.name,
            "category": app.category,
            "today_time": normal_time(int(total_seconds), "short"),
            "limit": limit,
            "status": int(total_seconds) < limit if limit else True
        })

    return apps_data
