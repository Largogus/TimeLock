from sqlalchemy.orm import Session
from core.models.App import App
from loguru import logger
import time


class AppCache:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._by_name = {}
        self._by_path = {}
        self._lock = False

    def load_all(self):
        if not self.session_factory:
            logger.error("AppCache: session_factory не установлен")
            return

        try:
            with self.session_factory() as session:
                apps = session.query(App).all()
                for app in apps:
                    self._by_name[app.name] = app
                    if app.path:
                        self._by_path[app.path] = app
                logger.success(f"AppCache: загружено {len(apps)} приложений")
        except Exception as e:
            logger.error(f"AppCache.load_all ошибка: {e}")

    def get_or_create(self, name: str, path: str):
        if not name:
            return None

        app = self._by_name.get(name) or self._by_path.get(path)
        if app:
            return app

        if self._lock:
            time.sleep(0.05)
            return self._by_name.get(name) or self._by_path.get(path)

        self._lock = True
        try:
            with self.session_factory() as session:
                app = session.query(App).filter(
                    (App.name == name) | (App.path == path)
                ).first()

                if not app:
                    app = App(name=name, path=path)
                    session.add(app)
                    session.flush()
                    session.commit()
                    logger.info(f"Добавлено новое приложение: {name}")

                self._by_name[app.name] = app
                if app.path:
                    self._by_path[app.path] = app

                return app

        except Exception as e:
            logger.error(f"AppCache.get_or_create ошибка для '{name}': {e}")
            return None
        finally:
            self._lock = False


app_cache = AppCache(None)