from sqlalchemy import func
from core.models.DailyStat import DailyStat
from datetime import datetime, timedelta


def get_middle_time(db_session_fabric, app_id: int) -> int:
    with db_session_fabric() as db_session:
        today = datetime.now().date()

        week_start = today - timedelta(days=6)

        rows = (
            db_session.query(
                func.coalesce(func.sum(
                    DailyStat.total_seconds
                ), 0
                ).label("total"),
                func.min(DailyStat.date).label("first_day"),
                func.count(DailyStat.id).label("active_days")
            )
            .filter(
                DailyStat.app_id == app_id,
                DailyStat.date.between(week_start, today)
            )
            .one()
        )

        total_seconds = rows.total or 0
        first_days = rows.first_day

        if first_days:
            days_count = (today - first_days).days + 1
            days_count = min(days_count, 7)
        else:
            days_count = 1

        middle_time = total_seconds / days_count

        return int(middle_time)