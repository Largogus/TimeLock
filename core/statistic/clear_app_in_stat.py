from core.models.App import App
from core.models.AppSession import AppSession
from core.models.DailyStat import DailyStat


def clear_app_in_stat(db_session, app_name):
    try:
        app = db_session.query(App).filter(App.name == app_name).first()

        if app:
            db_session.query(DailyStat).filter(
                DailyStat.app_id == app.id
            ).delete(synchronize_session=False)

            db_session.query(AppSession).filter(
                AppSession.app_id == app.id
            ).delete(synchronize_session=False)

        db_session.commit()

        return True, f"{app_name} успешно удалён из статистики"
    except Exception:
        db_session.rollback()
        return False, "Ошибка. Очистка не удалась"