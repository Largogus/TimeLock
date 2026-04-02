from datetime import datetime, date, time
from sqlalchemy import func

from core.models.AppLimit import AppLimit
from core.models.AppSession import AppSession
from core.system.config import SETTINGS


def can_limit(app, db_session):
    state_all_limit = SETTINGS.get("state_all_limit", 0)

    if not bool(state_all_limit):
        return True

    today_start = datetime.combine(date.today(), time.min)
    now = datetime.now()

    total_seconds = (
        db_session.query(
            func.coalesce(
                func.sum(
                    func.coalesce(
                        func.strftime(
                            '%s',
                            func.min(func.coalesce(AppSession.end_time, now), now)
                        ),
                        0
                    )
                    -
                    func.coalesce(
                        func.strftime(
                            '%s',
                            func.max(AppSession.start_time, today_start)
                        ),
                        0
                    )
                ),
                0
            )
        )
        .filter(
            AppSession.app_id == app.id,
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start,
        )
        .scalar()
    )

    limit = (
        db_session.query(AppLimit)
        .filter(AppLimit.app_id == app.id,
                AppLimit.enabled == 1,
                )
        .first()
    )

    if limit is None:
        return True

    if limit.daily_limit == 0:
        return True

    return total_seconds < limit.daily_limit