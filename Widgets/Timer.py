from PySide6.QtCore import QTimer, Signal


class Timer(QTimer):
    stopped = Signal()

    def stop(self):
        super().stop()
        self.stopped.emit()