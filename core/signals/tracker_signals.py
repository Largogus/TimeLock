from PySide6.QtCore import QObject, Signal
from core.db.session import SessionLocal


class TrackerSignalObject(QObject):
    appBlocked = Signal(str)
    sessionUpdate = Signal(int)
    errorOccurred = Signal(str)


signal = TrackerSignalObject()