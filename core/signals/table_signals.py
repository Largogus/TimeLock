from PySide6.QtCore import QObject, Signal


class TableSignalObject(QObject):
    objectCategoryChanged = Signal(str, str)


signal = TableSignalObject()