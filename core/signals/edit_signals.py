from PySide6.QtCore import QObject, Signal


class EditSignalObject(QObject):
    edit_or_delete_common_limit = Signal(int)
    upd_limit = Signal()


signal_edit = EditSignalObject()