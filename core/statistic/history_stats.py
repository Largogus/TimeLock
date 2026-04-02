from datetime import datetime, timedelta, date, time
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.models.App import App
from core.models.AppSession import AppSession
from sqlalchemy import select
from core.models.DailyStat import DailyStat


def get_history(session: Session):
    today_start = datetime.combine(date.today(), time.min)
    now = datetime.now()

    last_session_subq = (
        session.query(
            AppSession.app_id.label("app_id"),
            AppSession.start_time.label("last_start"),
            func.coalesce(AppSession.end_time, now).label("last_end"),
            func.row_number().over(
                partition_by=AppSession.app_id,
                order_by=AppSession.start_time.desc()
            ).label("rn")
        )
        .filter(
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start,
            func.strftime('%Y-%m-%d %H:%M', AppSession.start_time) !=
            func.strftime('%Y-%m-%d %H:%M', func.coalesce(AppSession.end_time, now))
        )
        .subquery()
    )

    total_seconds = func.sum(
        func.strftime('%s', func.min(func.coalesce(AppSession.end_time, now), now)) -
        func.strftime('%s', func.max(AppSession.start_time, today_start))
    )

    stats_query = (
        session.query(
            App.name,
            func.strftime('%H:%M', last_session_subq.c.last_start).label("start_time"),
            func.strftime('%H:%M', last_session_subq.c.last_end).label("end_time"),
            total_seconds.label("total_seconds"),
            func.count(AppSession.id).label("session_count")
        )
        .join(App, AppSession.app_id == App.id)
        .join(
            last_session_subq,
            (last_session_subq.c.app_id == App.id) &
            (last_session_subq.c.rn == 1)
        )
        .filter(
            func.strftime('%Y-%m-%d %H:%M', last_session_subq.c.last_start) !=
            func.strftime('%Y-%m-%d %H:%M', last_session_subq.c.last_end),
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start,
            App.status == "tracking"
        )
        .group_by(
            last_session_subq.c.last_end,
            last_session_subq.c.last_start
        )
        .all()
    )

    return stats_query


def get_history_session(session: Session, title: str):
    today_start = datetime.combine(date.today(), time.min)
    now = datetime.now()

    sessions_query = (
        session.query(
            (func.strftime('%s', func.coalesce(AppSession.end_time, now)) -
             func.strftime('%s', AppSession.start_time)).label("duration"),
            func.strftime('%H:%M', AppSession.start_time).label("start_time_str"),
            func.strftime('%H:%M', func.coalesce(AppSession.end_time, now)).label("end_time_str")
        )
        .join(App, AppSession.app_id == App.id)
        .filter(
            App.name == title,
            App.status == "tracking",
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start
        )
        .order_by(AppSession.start_time)
        .all()
    )

    return sessions_query