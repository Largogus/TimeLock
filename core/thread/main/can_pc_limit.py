from datetime import datetime, date, time
from sqlalchemy import func

from core.models.AppLimit import AppLimit
from core.models.AppSession import AppSession
from core.system.config import SETTINGS


def can_pc_limit(db_session):
    state_all_limit = SETTINGS.get("state_all_limit", 0)
    state_pc_limit = SETTINGS.get("state_limit_pc", 0)

    if not bool(state_pc_limit):
        return True

    if bool(state_pc_limit) and not bool(state_all_limit):
        return True

    today_start = datetime.combine(date.today(), time.min)
    now = datetime.now()

    limit_pc = SETTINGS.get("total_limit_pc", 43200)

    if limit_pc == 0:
        return True

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
            AppSession.start_time < now,
            func.coalesce(AppSession.end_time, now) > today_start,
        )
        .scalar()
    )

    return total_seconds < limit_pc