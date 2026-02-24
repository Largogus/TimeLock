from sqlalchemy import func
from datetime import datetime, date, time
from core.models.AppSession import AppSession


def get_total_pc_time_today(db_session) -> int:
    now = datetime.now()
    today_start = datetime.combine(date.today(), time.min)

    total_seconds = db_session.query(
        func.sum(
            func.strftime('%s', func.coalesce(AppSession.end_time, now)) -
            func.strftime('%s', AppSession.start_time)
        )
    ).filter(
        AppSession.start_time >= today_start
    ).scalar()

    return int(total_seconds or 0)