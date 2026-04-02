from PySide6.QtCore import QObject, Signal


class CoreEvents(QObject):
    settings_edited = Signal()
    app_added = Signal(str)
    show_visible = Signal()
    register_signal = Signal()

    remove_category = Signal(str)
    add_category = Signal(str)
    rename_category = Signal(str, str)


core_events = CoreEvents()