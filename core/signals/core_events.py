from PySide6.QtCore import QObject, Signal


class CoreEvents(QObject):
    settings_edited = Signal()
    app_added = Signal(str)
    show_visible = Signal()
    register_signal = Signal()


core_events = CoreEvents()