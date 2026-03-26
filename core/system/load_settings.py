from loguru import logger

from core.command.catergory_add_and_exists import add_base_category
from core.models.Settings import Setting
from core.db.session import SessionLocal


def load_settings(default_settings) -> dict:
    settings = {}

    with SessionLocal() as db_session:
        query = db_session.query(Setting).all()
        existing = {s.key: s for s in query}

        for key, value in default_settings.items():
            if key not in existing:
                logger.info(f"Добавляю настройку: {key}={value}")
                new_setting = Setting(key=key, value=str(value))
                db_session.add(new_setting)
                existing[key] = new_setting

        db_session.commit()

        add_base_category(db_session)

    for key, setting in existing.items():
        settings[key] = int(setting.value)

    return settings