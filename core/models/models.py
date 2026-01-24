from sqlalchemy import String, Integer, DateTime, ForeignKey, Column
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base import Base


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String)

    sessions = relationship(
        "Session",
        back_populates="app",
        cascade="all, delete-orphan"
    )

    limit = relationship(
        "AppLimit",
        uselist=False,
        back_populates="app",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<App(name={self.name})>"


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False)

    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Integer)

    app = relationship(
        "App",
        back_populates="sessions"
    )

    def __repr__(self):
        return f"<Session(app={self.app.name}, duration={self.duration})>"


class Blacklist(Base):
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False)

    app = relationship("App")

    def __repr__(self):
        return f"<Blacklist(app={self.app.name})>"


class AppLimit(Base):
    __tablename__ = "app_limits"

    app_id = Column(Integer, ForeignKey("apps.id"), primary_key=True)

    daily_limit = Column(Integer, nullable=False)
    enabled = Column(Integer, default=0)

    app = relationship("App", back_populates="limit")