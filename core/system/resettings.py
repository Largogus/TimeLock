from core.command.settings import set_settings
from core.models.Settings import Setting
from sqlalchemy import func
from sqlalchemy.orm import Session
from core.models.DailyStat import DailyStat


def resettings(db_session: Session):
    settings_bd = db_session.query(Setting).all()
    settings = {}

    for s in settings_bd:
        settings[s.key] = s.value

    settings.update({
        "tracking_interval_seconds": 1,
        "total_limit_pc": 0,
        "state_all_limit": 1,
        "state_limit_pc": 0,
        "focus": 0,
        "in_tray": 1,
        "show_notification": 1,
        "auto_start": 1,
        "keep_session": 1,
        "keep_archive": 31
    })

    for key, value in settings.items():
        set_settings(db_session, key, value, int)