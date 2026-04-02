from sqlalchemy import String, Integer, ForeignKey, Column
from sqlalchemy.orm import relationship
from core.db.base import Base


class FocusAllowed(Base):
    __tablename__ = "focus_allowed"

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=True)

    app = relationship(
        "App",
        back_populates="focus_allowed_entries"
    )

    def __repr__(self):
        return f"<FocusAllowed(app_id={self.app_id}, category={self.category})>"