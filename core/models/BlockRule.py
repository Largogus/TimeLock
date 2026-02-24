from sqlalchemy import (
    String, Integer, DateTime, ForeignKey,
    Column, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base import Base


class BlockRule(Base):
    __tablename__ = "block_rules"
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=True, index=True)
    reason = Column(String, nullable=False)
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)

    app = relationship("App", back_populates="block_rules")

    def __repr__(self):
        return f"<BlockRule(app_id={self.app_id}, reason={self.reason})>"