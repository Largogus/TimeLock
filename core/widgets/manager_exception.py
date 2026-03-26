from loguru import logger
from core.models.App import App
from core.signals.notification_signals import show_notification


def delete_exception(db_session, exception):
    try:
        query = (db_session.query(
                App
            )
            .filter(App.name == exception, App.status == "ignored")
            .first()
        )

        if query:
            query.status = "tracking"
            db_session.commit()
            show_notification.show_notification_app_tracking.emit(exception)
            return True, "Приложение снова отслеживается"
        else:
            return False, "Исключение не найдено"
    except Exception:
        db_session.rollback()
        logger.exception("Ошибка, приложение не получается отслеживать")
        return False, "Ошибка, приложение не получается отслеживать"


def add_exception(db_session, name):
    try:
        app = (db_session.query
           (
               App
           )
            .filter(App.name == name)
            .first()
        )

        if not app:
            return False, "Приложение уже отслеживается или не найдено"

        app.status = "ignored"

        db_session.commit()
        return True, "Приложение успешно добавлено в исключения"

    except Exception:
        db_session.rollback()
        logger.critical("Изменение не удалось")
        return False, "Не удалось добавить исключение"