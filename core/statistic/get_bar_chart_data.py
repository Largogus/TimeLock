from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.models.App import App
from core.models.DailyStat import DailyStat


def get_category_info(session: Session, period: str, target_date: datetime.date = None):
    if target_date is None:
        target_date = datetime.today().date()

    category_stats = {}
    stats_query = None

    if period == "Сегодня":
        stats_query = (
            session.query(
                App.category,
                func.sum(DailyStat.total_seconds).label("unfocus_seconds")
            )
            .join(App)
            .filter(DailyStat.date == target_date,
                    App.status == "tracking")
            .group_by(App.category)
            .all()
        )

    elif period == "Неделя":
        start_week = target_date - timedelta(days=6)
        end_week = target_date

        stats_query = (
            session.query(
                App.category,
                func.sum(DailyStat.total_seconds).label("unfocus_seconds")
            )
            .join(App)
            .filter(DailyStat.date >= start_week, DailyStat.date <= end_week,
                    App.status == "tracking")
            .group_by(App.category)
            .all()
        )

    elif period == "Месяц":
        start_month = target_date - timedelta(days=30)
        end_month = target_date

        stats_query = (
            session.query(
                App.category,
                func.sum(DailyStat.total_seconds).label("unfocus_seconds")
            )
            .join(App)
            .filter(DailyStat.date >= start_month, DailyStat.date <= end_month,
                    App.status == "tracking")
            .group_by(App.category)
            .all()
        )

    if stats_query is None:
        return False

    for category, total_seconds in stats_query:
        if total_seconds > 0:
            display_value, unit = get_display_value_and_unit(total_seconds)

            category_stats[category] = (display_value, total_seconds, unit)

    return category_stats


def get_app_info(session: Session, period: str, target_date: datetime.date = None):
    if target_date is None:
        target_date = datetime.today().date()

    app_stats = {}
    stats_query = None

    if period == "Сегодня":
        stats_query = (
            session.query(
                App.name,
                func.sum(DailyStat.total_seconds).label("unfocus_seconds")
            )
            .join(App)
            .filter(DailyStat.date == target_date,
                    App.status == "tracking")
            .group_by(App.name)
            .all()
        )
    elif period == "Неделя":
        start_week = target_date - timedelta(days=6)
        end_week = target_date

        stats_query = (
            session.query(
                App.name,
                func.sum(DailyStat.total_seconds).label("unfocus_seconds")
            )
            .join(App)
            .filter(DailyStat.date >= start_week, DailyStat.date <= end_week,
                    App.status == "tracking")
            .group_by(App.name)
            .all()
        )

    elif period == "Месяц":
        start_month = target_date - timedelta(days=30)
        end_month = target_date

        stats_query = (
            session.query(
                App.name,
                func.sum(DailyStat.total_seconds).label("unfocus_seconds")
            )
            .join(App)
            .filter(DailyStat.date >= start_month, DailyStat.date <= end_month,
                    App.status == "tracking")
            .group_by(App.name)
            .all()
        )

    if stats_query is None:
        return False

    for app, total_seconds in stats_query:
        if total_seconds > 59:
            formt = total_seconds // 60

            display_value, unit = get_display_value_and_unit(total_seconds)

            app_stats[app] = (display_value, formt, unit)

    return app_stats


def get_display_value_and_unit(total_seconds):
    if total_seconds < 3600:
        display_value = total_seconds // 60
        unit = "мин"
    else:
        display_value = round(total_seconds / 3600, 1)
        unit = "ч"

    return display_value, unit