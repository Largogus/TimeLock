from loguru import logger
from core.models.App import App
from core.models.CategoryLimit import CategoryLimit


def delete_category(db_session, category_name):
    try:
        apps_exist = db_session.query(App).filter(App.category == category_name).first()

        if apps_exist:
            return False, "В категории есть приложения. Удаление невозможно"

        query = (db_session.query(
                CategoryLimit
            )
            .filter(CategoryLimit.category_name == category_name)
            .first()
        )

        if query:
            db_session.delete(query)
            db_session.commit()
            return True, "Категория успешно удалена"
        else:
            return False, "Категория не найдена"

    except Exception:
        db_session.rollback()
        logger.exception("Ошибка удаления категории")
        return False, "Ошибка при удалении категории"


def add_category(db_session, category_name):
    try:
        exists = (db_session.query(
            CategoryLimit
            )
            .filter(CategoryLimit.category_name == category_name)
            .first()
        )

        if exists:
            return False, "Категория уже существует"

        new_category = CategoryLimit(category_name=category_name,
                                     limit_seconds=None,
                                     enabled=1)

        if new_category:
            db_session.add(new_category)
            db_session.commit()
            return True, "Категория успешно добавлена"
    except Exception:
        db_session.rollback()
        logger.exception("Ошибка при добавлении категории")


def change_category(db_session, last_name, category_name):
    try:
        category = (db_session.query(
            CategoryLimit
            )
            .filter(CategoryLimit.category_name == last_name)
            .first()
        )

        if category:
            category.category_name = category_name
            db_session.commit()
            return True, "Название успешно изменено"
    except Exception:
        db_session.rollback()
        logger.exception("Название не удалось изменить")