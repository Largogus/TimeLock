from loguru import logger


class ThreadManager:
    def __init__(self):
        self._threads = []

    def register(self, thread):
        self._threads.append(thread)
        return thread

    def stop_all(self):
        logger.info("Останавливаем все потоки...")

        for thread in self._threads:
            try:
                thread.requestInterruption()
            except Exception:
                logger.exception("Ошибка requestInterruption")

        for thread in self._threads:
            try:
                thread.wait()
            except Exception:
                logger.exception("Ошибка wait")

        logger.success("Все потоки остановлены")


thread_manager = ThreadManager()