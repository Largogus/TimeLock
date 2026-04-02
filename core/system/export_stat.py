import csv
import zipfile
from io import StringIO, BytesIO

from core.models.App import App
from core.models.AppSession import AppSession
from core.models.DailyStat import DailyStat


def export_statistics(db_session):

    stats_archive = (
        db_session.query(DailyStat, App.name)
        .join(App, DailyStat.app_id == App.id)
        .all()
    )

    stats_session = (
        db_session.query(AppSession, App.name)
        .join(App, AppSession.app_id == App.id)
        .all()
    )

    csv_archive = StringIO()
    writer_archive = csv.writer(csv_archive)

    writer_archive.writerow([
        "date",
        "app_name",
        "total_seconds",
        "sessions_count",
        "focus_seconds",
        "focus_count"
    ])

    for stat, app_name in stats_archive:
        writer_archive.writerow([
            stat.date,
            app_name,
            stat.total_seconds,
            stat.sessions_count,
            stat.focus_seconds,
            stat.focus_count
        ])

    csv_session = StringIO()
    writer_session = csv.writer(csv_session)

    writer_session.writerow([
        "app_name",
        "start_time",
        "end_time",
        "focus_mode"
    ])

    for session, app_name in stats_session:
        writer_session.writerow([
            app_name,
            session.start_time,
            session.end_time,
            session.focus_mode
        ])

    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("daily_stats.csv", csv_archive.getvalue())
        z.writestr("sessions.csv", csv_session.getvalue())

    zip_buffer.seek(0)

    return zip_buffer