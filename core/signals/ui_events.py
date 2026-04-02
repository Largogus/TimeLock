from PySide6.QtCore import QObject, Signal


class UIEvents(QObject):
    show_limit_modal = Signal(str, int)
    show_focus_notification = Signal(str, int)
    show_limit_pc = Signal()
    show_blocked_user_modal = Signal(str, int)


ui_events = UIEvents()