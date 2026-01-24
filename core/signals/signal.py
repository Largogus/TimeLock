from PySide6.QtCore import QObject, Signal


class SignalObject(QObject):
    change_window = Signal(str)
    minutes = Signal(int)