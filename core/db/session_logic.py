from core.models.App import App
from core.models.AppSession import AppSession
from core.db.session import SessionLocal
from datetime import datetime


def handle_session(app: App, db_session: SessionLocal):
    active_session = db_session.query(AppSession).filter_by(end_time=None).first()

    if active_session and active_session.app_id == app.id:
        return

    if active_session:
        active_session.end_time = datetime.now()

    new_session = AppSession(
        app_id=app.id,
        start_time=datetime.now()
    )

    db_session.add(new_session)
    db_session.commit()


def close_session(db_session: SessionLocal):
    now = datetime.now()

    open_sessions = (
        db_session.query(AppSession)
        .filter(AppSession.end_time.is_(None))
        .all()
    )

    for session in open_sessions:
        session.end_time = now

    db_session.commit()