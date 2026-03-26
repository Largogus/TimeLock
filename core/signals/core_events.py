from PySide6.QtCore import QObject, Signal


class CoreEvents(QObject):
    settings_edited = Signal()


core_events = CoreEvents()