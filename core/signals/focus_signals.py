from PySide6.QtCore import QObject, Signal


class FocusSignals(QObject):
    startFocus = Signal(bool)


signal = FocusSignals()