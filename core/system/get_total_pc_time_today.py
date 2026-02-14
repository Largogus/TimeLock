from sqlalchemy import func, case
from datetime import datetime, date
from core.models.models import AppSession


def get_total_pc_time_today(db_session) -> int:
    today_start = datetime.combine(date.today(), datetime.min.time())
    now = datetime.now()

    sessions = db_session.query(AppSession).filter(AppSession.start_time >= today_start).all()

    total_seconds = 0
    for s in sessions:
        end_time = s.end_time or now
        delta = end_time - s.start_time
        total_seconds += int(delta.total_seconds())

    return int(total_seconds)