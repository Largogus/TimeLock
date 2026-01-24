from PySide6.QtCore import QThread, Signal
from psutil import boot_time
from time import time, sleep


class CountWindowsLife(QThread):
    tick = Signal(int)

    def __init__(self):
        super().__init__()
        self.uptime_start = int(time() - boot_time())
        self._running = True

    def run(self):
        while self._running:
            current_time = int(time() - boot_time())

            self.tick.emit(current_time)

            sleep(1)

    def stop(self):
        self._running = False
        self.wait()