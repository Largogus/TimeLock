from core.db.base import Base
from core.db.engine import engine


def init_db():
    Base.metadata.create_all(bind=engine)