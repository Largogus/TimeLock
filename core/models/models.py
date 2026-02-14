from sqlalchemy import String, Integer, DateTime, ForeignKey, Column, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from core.db.base import Base


class App(Base):
    __tablename__ = "apps"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    path = Column(String)
    category = Column(String)

    sessions = relationship("AppSession", back_populates="app", cascade="all, delete-orphan")
    limit = relationship("AppLimit", back_populates="app", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<App(name={self.name})>"


class AppSession(Base):
    __tablename__ = "app_sessions"

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False, index=True)

    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, index=True)

    app = relationship("App", back_populates="sessions")

    def __repr__(self):
        app_name = self.app.name if self.app else "Unknown"
        return f"<AppSession(name={app_name})>"


class PcSession(Base):
    __tablename__ = "pc_sessions"

    id = Column(Integer, primary_key=True)

    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, index=True)

    is_idle = Column(Boolean, default=False)


class AppLimit(Base):
    __tablename__ = "app_limits"

    app_id = Column(Integer, ForeignKey("apps.id"), primary_key=True)

    daily_limit_minutes = Column(Integer, nullable=True)
    is_blocked = Column(Boolean, default=False)
    enabled = Column(Boolean, default=True)

    app = relationship("App", back_populates="limit")

    def __repr__(self):
        app_name = self.app.name if self.app else "Unknown"
        return f"<AppSession(name={app_name})>"


class DailyStat(Base):
    __tablename__ = "daily_stats"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, index=True)
    app_id = Column(Integer, ForeignKey("apps.id"), nullable=False)

    total_seconds = Column(Integer, default=0)
    sessions_count = Column(Integer, default=0)

    app = relationship("App")

    def __repr__(self):
        app_name = self.app.name if self.app else "Unknown"
        return f"<AppSession(name={app_name})>"


class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True)
    value = Column(String, nullable=False)