from sqlalchemy import Integer, ForeignKey, Column, Boolean
from sqlalchemy.orm import relationship
from core.db.base import Base


class AppLimit(Base):
    __tablename__ = "app_limits"

    app_id = Column(Integer, ForeignKey("apps.id"), primary_key=True)

    daily_limit = Column(Integer, nullable=True)
    enabled = Column(Boolean, default=True)

    app = relationship("App", back_populates="limit")

    def __repr__(self):
        app_name = self.app.name if self.app else "Unknown"
        return f"<AppLimit(name={app_name})>"