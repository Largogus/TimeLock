from sqlalchemy import (
    String, Integer, DateTime, ForeignKey,
    Column, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base import Base


class BlockApp(Base):
    __tablename__ = "block_app"
    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=True, index=True)
    blocked = Column(Integer, nullable=True)

    app = relationship("App", back_populates="block_app")

    def __repr__(self):
        return f"<BlockApp(app_id={self.app_id}>"