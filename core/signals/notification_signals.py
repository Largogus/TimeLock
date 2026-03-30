from PySide6.QtCore import QObject, Signal


class NotificationSignals(QObject):
    show_notification_blocked = Signal(str)
    show_notification_unblocked = Signal(str)
    show_notification_app_not_tracking = Signal(str)
    show_notification_app_tracking = Signal(str)
    show_notification_error_limit = Signal(str, int)
    show_notification_focus_off = Signal()
    show_notification_focus_on = Signal()


show_notification = NotificationSignals()