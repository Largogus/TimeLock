from sqlalchemy import Integer, DateTime, Column, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base import Base


class FocusSession(Base):
    __tablename__ = "focus_sessions"

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    focus_allowed_entries = relationship(
        "FocusAllowed",
        back_populates="focus_session",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<FocusSession(id={self.id}, active={self.is_active})>"