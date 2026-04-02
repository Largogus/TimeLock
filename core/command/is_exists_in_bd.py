from core.models.App import App


def is_exists_in_bd(db_session, app):
    session = db_session.query(App).filter(App.name == app).first()

    if session is not None:
        return True
    else:
        return False