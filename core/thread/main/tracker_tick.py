from datetime import datetime
from core.db.session_logic import handle_session
from core.system.windows_active_app import get_active_window_app
from core.models.App import App
from core.db.session import SessionLocal
from core.thread.main.can_limit import can_limit
from sqlalchemy import or_


_apps_by_name = {}
_apps_by_path = {}


def tracker_tick(db_session: SessionLocal):
    active_app_name, active_app_path = get_active_window_app()

    if not active_app_name: return

    app = _apps_by_name.get(active_app_name)

    if not app:
        app = _apps_by_path.get(active_app_path)

    if not app:
        app = (
            db_session.query(App)
            .filter(or_(
                App.name == active_app_name,
                App.path == active_app_path))
            .first())

        if not app:
            app = App(name=active_app_name, path=active_app_path)
            db_session.add(app)
            db_session.commit()

        _apps_by_name[app.name] = app
        _apps_by_path[app.path] = app

    if not can_limit(app, db_session):
        return print("ЛИМИТ АЛО")

    handle_session(app, db_session)

    return active_app_name, active_app_path