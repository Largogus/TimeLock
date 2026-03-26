from loguru import logger
from sqlalchemy.orm import Session
from core.models.DailyStat import DailyStat
from core.models.App import App
from core.models.AppSession import AppSession
from core.models.AppLimit import AppLimit
from core.models.FocusAllowed import FocusAllowed
from core.models.CategoryLimit import CategoryLimit
from core.models.BlockApp import BlockApp
from core.models.Settings import Setting
from core.system.resettings import resettings


def delete_all_info(db_session: Session):
    tables = [AppSession, FocusAllowed, BlockApp, CategoryLimit, AppLimit, App, DailyStat, Setting]
    try:
        for table in tables:
            db_session.query(table).delete(synchronize_session=False)

        db_session.commit()

        resettings(db_session)

        logger.success("Вся информация стёрта успешно")

        return True, "Вся информация стёрта успешно"
    except Exception:
        db_session.rollback()
        logger.exception("Не удалось стереть данные")
        return False, "Не удалось стереть данные"