from loguru import logger

from core.models.CategoryLimit import CategoryLimit


def add_base_category(db_session):
    is_exists = (db_session.query(
            CategoryLimit
        )
        .filter(CategoryLimit.category_name == "Без категории")
    ).first()

    if is_exists:
        return
    else:
        try:
            base_category = CategoryLimit(
                category_name="Без категории")

            db_session.add(base_category)
            db_session.commit()
            logger.info("Добавлен системный элемент")
        except Exception as e:
            db_session.rollback()
            logger.exception(f"Отсутсвует критически важный элемент: {e}")