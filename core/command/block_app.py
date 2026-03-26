from core.models.App import App
from core.models.BlockApp import BlockApp
from core.signals.notification_signals import show_notification
from loguru import logger


def add_block_app(name, db_session):
    try:
        blocked_app = (db_session.query(
            BlockApp
        )
                       .join(BlockApp.app)
                       .filter(App.name == name)
                       .first()
                       )

        if not blocked_app:
            app = db_session.query(App).filter(App.name == name).first()
            if not app:
                logger.warning(f"Приложение '{name}' не найдено в базе")
                return

            new_block = BlockApp(app=app, blocked=1)
            db_session.add(new_block)
            db_session.commit()
            logger.info(f"Приложение '{name}' заблокировано")
            show_notification.show_notification_blocked.emit(name)

    except Exception:
        db_session.rollback()
        logger.exception("Добавление не удалось")


def remove_block_app(name, db_session):
    try:
        blocked_app = (db_session.query(
            BlockApp
        )
                       .join(BlockApp.app)
                       .filter(App.name == name)
                       .first()
                       )

        if blocked_app:
            db_session.delete(blocked_app)
            db_session.commit()
            logger.info(f"Приложение '{name}' разблокировано")
            show_notification.show_notification_unblocked.emit(name)
    except Exception:
        db_session.rollback()
        logger.exception("Удаление не удалось")


def is_blocked(app, db_session, app_is_name: bool = False):
    if app_is_name:
        name = db_session.query(App).filter(App.name == app).first()
        if not app:
            logger.warning(f"Приложение '{app}' не найдено в базе")
            return

        app = name

    is_blocked = (db_session.query(
            BlockApp
        )
        .filter(
            BlockApp.app_id == app.id,
            BlockApp.blocked == 1
        )
        .first()
    )

    if is_blocked is None:
        return False

    return True