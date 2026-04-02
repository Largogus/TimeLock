from core.signals.notification_signals import show_notification
from core.signals.ui_events import ui_events
from core.system.config import SETTINGS

_connected_slots = {}


def connect_notifications(manager):
    global _connected_slots

    if not SETTINGS.get('show_notification', 1):
        if _connected_slots != {}:
            for signal, slot in _connected_slots.items():
                try:
                    signal.disconnect(slot)
                except (TypeError, RuntimeError):
                    pass
            _connected_slots.clear()

        return

    for signal, slot in _connected_slots.items():
        try:
            signal.disconnect(slot)
        except (TypeError, RuntimeError):
            pass
    _connected_slots.clear()

    slot = lambda name, hwnd: manager.show(
        "У вас запущен фокус, %app% свёрнут",
        name,
        hwnd
    )
    ui_events.show_focus_notification.connect(slot)
    _connected_slots[ui_events.show_focus_notification] = slot

    slot = lambda name: manager.show("%app% разблокирован", name)
    show_notification.show_notification_unblocked.connect(slot)
    _connected_slots[show_notification.show_notification_unblocked] = slot

    slot = lambda name: manager.show("%app% заблокирован", name)
    show_notification.show_notification_blocked.connect(slot)
    _connected_slots[show_notification.show_notification_blocked] = slot

    slot = lambda name: manager.show(
        "%app% больше не отслеживатеся, снова отслеживать можете в Настройки",
        name
    )
    show_notification.show_notification_app_not_tracking.connect(slot)
    _connected_slots[show_notification.show_notification_app_not_tracking] = slot

    slot = lambda name: manager.show("%app% снова отслеживатеся", name)
    show_notification.show_notification_app_tracking.connect(slot)
    _connected_slots[show_notification.show_notification_app_tracking] = slot

    slot = lambda name, time: manager.show(
        f"Лимит для %app% не может быть меньше {time} минут",
        name
    )
    show_notification.show_notification_error_limit.connect(slot)
    _connected_slots[show_notification.show_notification_error_limit] = slot

    slot = lambda: manager.show("Время работы в фокусе истекло")
    show_notification.show_notification_focus_off.connect(slot)
    _connected_slots[show_notification.show_notification_focus_off] = slot

    slot = lambda: manager.show("Время работы в фокусе запущено")
    show_notification.show_notification_focus_on.connect(slot)
    _connected_slots[show_notification.show_notification_focus_on] = slot