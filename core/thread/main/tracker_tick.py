from loguru import logger
from core.system.windows_active_app import get_active_window_app
from core.command.block_app import is_blocked
from core.db.session_logic import handle_session
from core.signals.ui_events import ui_events
from core.thread.main.can_category_limit import can_category_limit
from core.thread.main.can_pc_limit import can_pc_limit
from core.thread.main.check_and_handle_focus import check_and_handle_focus
from core.thread.main.can_limit import can_limit
from core.system.app_cache import app_cache


def tracker_tick(db_session):
    active_app_name, active_app_path, proc, hwnd = get_active_window_app()

    if not active_app_name:
        return None, None, None, None

    app = app_cache.get_or_create(active_app_name, active_app_path)

    if not app:
        logger.warning(f"Не удалось получить/создать app для {active_app_name}")
        return None, None, None, None

    if not can_pc_limit(db_session):
        ui_events.show_limit_pc.emit()
        return None, None, None, None

    if is_blocked(app, db_session):
        ui_events.show_blocked_user_modal.emit(app.name, hwnd)
        return None, None, None, None

    if check_and_handle_focus(app, hwnd, db_session):
        handle_session(app, db_session, focus=1)
        return None, None, None, None

    if not can_limit(app, db_session):
        ui_events.show_limit_modal.emit(app.name, hwnd)
        return None, None, None, None

    if not can_category_limit(app, db_session):
        ui_events.show_limit_modal.emit(app.name, hwnd)
        return None, None, None, None

    return app, hwnd, active_app_name, active_app_path