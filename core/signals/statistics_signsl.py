from PySide6.QtCore import QObject, Signal


class StatisticsSignalObject(QObject):
    upd_stats = Signal()
    upd_history = Signal()
    click_period = Signal(str)
    thread_upd_history = Signal(list)
    thread_upd_stats = Signal(list, dict, dict)


stats_signal = StatisticsSignalObject()