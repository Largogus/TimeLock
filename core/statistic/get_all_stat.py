from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session
from core.models.DailyStat import DailyStat


def get_all_stats(session: Session, period: str, target_date: datetime.date = None):
    if target_date is None:
        target_date = datetime.today().date()

    total_time = 0
    time_in_focus = 0
    session_count = 0
    stats_query = None

    if period == "Сегодня":
        stats_query = (
            session.query(
                func.sum(DailyStat.total_seconds).label("unfocus_seconds"),
                func.sum(DailyStat.focus_seconds).label("focus_seconds"),
                func.sum(DailyStat.sessions_count).label("session")
            )
            .filter(DailyStat.date == target_date)
            .all()
        )

    elif period == "Неделя":
        start_week = target_date - timedelta(days=6)
        end_week = target_date

        stats_query = (
            session.query(
                func.sum(DailyStat.total_seconds).label("unfocus_seconds"),
                func.sum(DailyStat.focus_seconds).label("focus_seconds"),
                func.sum(DailyStat.sessions_count).label("session")
            )
            .filter(DailyStat.date >= start_week, DailyStat.date <= end_week)
            .all()
        )

    elif period == "Месяц":
        start_week = target_date - timedelta(days=30)
        end_week = target_date

        stats_query = (
            session.query(
                func.sum(DailyStat.total_seconds).label("unfocus_seconds"),
                func.sum(DailyStat.focus_seconds).label("focus_seconds"),
                func.sum(DailyStat.sessions_count).label("session")
            )
            .filter(DailyStat.date >= start_week, DailyStat.date <= end_week)
            .all()
        )

    if stats_query is None:
        return False

    for total_sec, focus_sec, ses_count in stats_query:
        session_count += ses_count or 0
        total_time += total_sec or 0
        time_in_focus += focus_sec or 0

    time_without_focus = total_time - time_in_focus

    return total_time, time_in_focus, time_without_focus, session_count
