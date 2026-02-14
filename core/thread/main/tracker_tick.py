from datetime import datetime
from core.db.session_logic import handle_session
from core.system.windows_active_app import get_active_window_app
from core.models.models import App
from core.db.session import SessionLocal
from core.thread.main.can_limit import can_limit


def tracker_tick(db_session: SessionLocal):
    active_app_name, active_app_path = get_active_window_app()

    if not active_app_name:
        return

    app = db_session.query(App).filter_by(name=active_app_name).first()
    exe = db_session.query(App).filter_by(path=active_app_path).first()

    if not app and not exe:
        app = App(name=active_app_name, path=active_app_path)
        db_session.add(app)
        db_session.commit()
    elif not app and exe:
        app = db_session.query(App).filter_by(path=active_app_path).first()
        active_app_name = exe.name

    if not can_limit(app, db_session):
        return print("ЛИМИТ АЛО")

    handle_session(app, db_session)

    return active_app_name