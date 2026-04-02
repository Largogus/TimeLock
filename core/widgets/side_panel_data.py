from datetime import datetime
from sqlalchemy import and_, func
from core.db.session import SessionLocal
from core.models.App import App
from core.models.AppSession import AppSession
from core.models.CategoryLimit import CategoryLimit
from core.system.date import normal_time


def addData(category_name: str) -> tuple[str, int, dict]:
    with SessionLocal() as session:
        start_of_day = datetime.combine(datetime.today(), datetime.min.time())
        now = datetime.now()

        data = session.query(AppSession).join(App).filter(
            App.category == category_name,
            AppSession.start_time <= now,
            func.coalesce(AppSession.end_time, now) >= start_of_day,
            App.status == "tracking"
        )

        total_time = 0
        top_apps = {}
        data_limit = session.query(CategoryLimit).filter(CategoryLimit.category_name == category_name).first()
        limits = data_limit.limit_seconds

        for s in data:
            real_start = max(s.start_time, start_of_day)
            real_end = min(s.end_time or now, now)

            seconds = int((real_end - real_start).total_seconds())

            if seconds < 0:
                continue

            total_time += seconds
            app_name = s.app.name if s.app else "Unknown"
            top_apps[app_name] = top_apps.get(app_name, 0) + seconds

        text = f"Сегодня: {normal_time(total_time, format='short')} / Лимит: {normal_time(limits, format='short') if limits is not None else 'Нет'}"

        top_apps = dict(sorted(top_apps.items(), key=lambda x: x[1], reverse=True))

        return text, limits, top_apps