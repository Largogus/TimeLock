from sqlalchemy import func
from datetime import datetime, date, time

from core.db.session import SessionLocal
from core.models.App import App
from core.models.AppSession import AppSession


def get_total_pc_time_today() -> int:
    with SessionLocal() as db_session:
        now = datetime.now()
        today_start = datetime.combine(date.today(), time.min)

        total_seconds = (db_session.query(
            func.sum(
                func.strftime(
                    '%s',
                    func.min(func.coalesce(AppSession.end_time, now), now)
                ) -
                func.strftime(
                    '%s',
                    func.max(AppSession.start_time, today_start)
                )
            )
        ).join(App)
         .filter(
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start,
            App.status == "tracking"
        ).scalar())

        return int(total_seconds or 0)