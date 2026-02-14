from loguru import logger
from core.models.models import Setting


def get_settings(db_session, key, cast_type):
    settings = db_session.query(Setting).filter_by(key=key).first()

    if not settings:
        logger.warning("Ключ не обнаружен")
        return
    else:
        settings_value = cast_type(settings.value)
        return settings_value


def set_settings(db_session, key, value, cast_type):
    settings = db_session.query(Setting).filter_by(key=key).first()

    if not settings:
        settings = Setting(key=key, value=value)
        db_session.add(settings)
    else:
        settings.value = cast_type(value)

    db_session.commit()
