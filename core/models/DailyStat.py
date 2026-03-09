from sqlalchemy import Integer, ForeignKey, Column, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base import Base


class DailyStat(Base):
    __tablename__ = "daily_stats"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False)

    total_seconds = Column(Integer, default=0)
    sessions_count = Column(Integer, default=0)

    focus_seconds = Column(Integer, default=0)
    focus_count = Column(Integer, default=0)

    app = relationship("App")

    def __repr__(self):
        app_name = self.app.name if self.app else "Unknown"
        return f"<AppSession(name={app_name})>"