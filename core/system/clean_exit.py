from datetime import datetime
from loguru import logger
from core.command.settings import set_settings
from core.db.session import SessionLocal
from core.models.AppSession import AppSession
from core.system.mutex import single_instance
from core.widgets.thread_manager import thread_manager


def clean_exit(overlays, modal):
    thread_manager.stop_all()
    single_instance.release()

    if modal and modal.isVisible():
        modal.close()

    for ov in overlays:
        if ov.isVisible():
            ov.close()

    with SessionLocal() as s:
        close_active_sessions()
        set_settings(s, "focus", 0, int)


def close_active_sessions():
    with SessionLocal() as db_session:
        try:
            now = datetime.now()

            db_session.query(AppSession).filter(
                AppSession.end_time.is_(None)
            ).update({
                AppSession.end_time: now
            }, synchronize_session=False)

            db_session.commit()
            logger.info("Все активные сессии корректно закрыты при выходе")
        finally:
            db_session.close()