from core.command.block_app import is_blocked
from core.db.session_logic import handle_session
from core.signals.ui_events import ui_events
from core.system.windows_active_app import get_active_window_app
from core.models.App import App
from core.db.session import SessionLocal
from core.thread.main.can_category_limit import can_category_limit
from core.thread.main.can_pc_limit import can_pc_limit
from core.thread.main.check_and_handle_focus import check_and_handle_focus
from core.thread.main.can_limit import can_limit
from sqlalchemy import or_


_apps_by_name = {}
_apps_by_path = {}
_modal_open = False


def tracker_tick(db_session: SessionLocal):
    global _modal_open

    active_app_name, active_app_path, proc, hwnd = get_active_window_app()

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

    if not can_pc_limit(db_session):
        ui_events.show_limit_pc.emit()
        return

    if is_blocked(app, db_session):
        ui_events.show_blocked_user_modal.emit(app.name, hwnd)
        return

    if check_and_handle_focus(app, hwnd, db_session):
        handle_session(app, db_session, focus=1)
        return

    if not can_limit(app, db_session):
        ui_events.show_limit_modal.emit(app.name, hwnd)
        return

    if not can_category_limit(app, db_session):
        ui_events.show_limit_modal.emit(app.name, hwnd)
        return

    handle_session(app, db_session)

    return active_app_name, active_app_path