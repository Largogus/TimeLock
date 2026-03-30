from loguru import logger
from core.models.Settings import Setting
from core.signals.core_events import core_events


def set_settings(db_session, key, value, cast_type):
    settings = db_session.query(Setting).filter_by(key=key).first()

    if not settings:
        settings = Setting(key=key, value=value)
        db_session.add(settings)
    else:
        settings.value = cast_type(value)

    db_session.commit()
    core_events.settings_edited.emit()

    logger.debug("Настройки изменились")

    return True
