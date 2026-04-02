from sqlalchemy import String, Integer, Column, Boolean
from core.db.base import Base


class CategoryLimit(Base):
    __tablename__ = "category_limits"

    id = Column(Integer, primary_key=True)
    category_name = Column(String, unique=True, nullable=False)
    limit_seconds = Column(Integer)
    enabled = Column(Boolean, default=True)

    def __repr__(self):
        return f"<CategoryLimit(category={self.category_name}, limit={self.limit_seconds})>"