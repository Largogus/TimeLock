from time import time
from threading import Thread
from typing import List, Union

from PySide6.QtCore import QThread
from loguru import logger


class ThreadManager:
    def __init__(self):
        self._threads: List[Union[QThread, Thread]] = []
        self._db_writer = None

    def register(self, thread):
        if thread not in self._threads:
            self._threads.append(thread)
            logger.success(f"ThreadManager: зарегистрирован поток {thread.__class__.__name__}")
        return thread

    def register_db_writer(self, db_writer):
        self._db_writer = db_writer
        logger.success("ThreadManager: DBWriter зарегистрирован")

    def stop_all(self, timeout: int = 5):
        logger.info("Останавливаем все потоки...")

        for thread in self._threads:
            try:
                if hasattr(thread, 'requestInterruption'):
                    thread.requestInterruption()
                elif hasattr(thread, 'stop'):
                    thread.stop()
                elif hasattr(thread, 'quit'):
                    thread.quit()
            except Exception as e:
                logger.warning(f"Не удалось отправить stop сигнал потоку {thread}: {e}")

        if self._db_writer:
            try:
                self._db_writer.stop()
            except Exception as e:
                logger.warning(f"Ошибка остановки DBWriter: {e}")

        start_time = time()
        for thread in self._threads:
            try:
                if hasattr(thread, 'wait'):
                    thread.wait(timeout * 1000)
                elif hasattr(thread, 'join'):
                    thread.join(timeout=timeout)
            except Exception as e:
                logger.warning(f"Ошибка ожидания потока: {e}")

        elapsed = time() - start_time
        logger.success(f"ThreadManager: все потоки остановлены за {elapsed:.2f} сек")

    def clear(self):
        self._threads.clear()
        self._db_writer = None


thread_manager = ThreadManager()