from queue import Queue, Empty
from threading import Thread
import time
from loguru import logger
from sqlalchemy.exc import OperationalError
from core.db.session import SessionLocal


class DBWriter:
    def __init__(self):
        self.queue: Queue = Queue(maxsize=250)
        self.worker: Thread | None = None
        self.running = False

    def start(self):
        if self.worker and self.worker.is_alive():
            return

        self.running = True
        self.worker = Thread(target=self._worker_loop, daemon=True, name="DBWriter-Thread")
        self.worker.start()
        logger.success("DBWriter успешно запущен — все записи теперь асинхронные")

    def stop(self):
        self.running = False
        if self.worker:
            self.queue.put(None)
            self.worker.join(timeout=5)

    def _worker_loop(self):
        while self.running:
            try:
                task = self.queue.get(timeout=1.0)

                if task is None:
                    break

                func, args, kwargs = task

                for attempt in range(7):
                    try:
                        with SessionLocal() as session:
                            result = func(session, *args, **kwargs)
                            session.commit()
                        break

                    except OperationalError as e:
                        if "database is locked" in str(e).lower():
                            delay = min(0.3 * (attempt + 1), 2.0)
                            time.sleep(delay)
                            continue
                        else:
                            logger.error(f"DBWriter OperationalError: {e}")
                            break

                    except Exception as e:
                        logger.error(f"DBWriter ошибка при выполнении задачи: {e}")
                        break

            except Empty:
                continue
            except Exception as e:
                logger.error(f"DBWriter queue error: {e}")

    def submit(self, func, *args, **kwargs):
        try:
            self.queue.put_nowait((func, args, kwargs))
        except:
            logger.warning("DBWriter: очередь переполнена, задача потеряна")


db_writer = DBWriter()