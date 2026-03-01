from sqlalchemy import Integer, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship
from core.db.base import Base


class FocusSession(Base):
    __tablename__ = "focus_session"

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False, index=True)

    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, index=True)

    app = relationship("App", back_populates="sessions")

    def __repr__(self):
        app_name = self.app.name if self.app else "Unknown"
        return f"<AppSession(name={app_name})>"