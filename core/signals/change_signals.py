from PySide6.QtCore import QObject, Signal


class ChangeSignalObject(QObject):
    application_screen = Signal(int, str)
    application_arg = Signal(str)

    limit_screen = Signal(int, str, str)
    limit_app = Signal(str)
    limit_category = Signal(str)


signal_change = ChangeSignalObject()