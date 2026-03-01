from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import relationship
from core.db.base import Base
from core.models.BlockRule import BlockRule
from core.models.FocusAllowed import FocusAllowed


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String)
    category = Column(String, nullable=False, default="Без категории")
    status = Column(String, nullable=False, default="tracking")

    sessions = relationship("AppSession", back_populates="app", cascade="all, delete-orphan")
    limit = relationship("AppLimit", back_populates="app", uselist=False, cascade="all, delete-orphan")
    block_rules = relationship("BlockRule", back_populates="app", cascade="all, delete-orphan")
    focus_allowed_entries = relationship("FocusAllowed", back_populates="app", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<App(name={self.name})>"