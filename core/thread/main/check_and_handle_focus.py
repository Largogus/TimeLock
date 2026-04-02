from core.models.App import App
from core.models.FocusAllowed import FocusAllowed
from core.signals.ui_events import ui_events
from core.system.config import SETTINGS
from core.system.windows_active_app import is_safe_window


def check_and_handle_focus(app, hwnd, db_session):
    state_focus = SETTINGS.get("focus", 0)

    if not bool(state_focus):
        return False

    if not is_safe_window(hwnd):
        return True

    focus = (
        db_session.query(FocusAllowed)
        .join(App)
        .filter(
            FocusAllowed.app_id == app.id
        )
        .first()
    )

    if focus is None:
        ui_events.show_focus_notification.emit(app.name, hwnd)
        return False

    return True