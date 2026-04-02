from sqlalchemy import create_engine, event
from core.system.config import DATABASE_PATH


engine = create_engine(
    DATABASE_PATH,
    connect_args={"check_same_thread": False, "timeout": 10.0},
    echo=False,
    pool_pre_ping=True
)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=10000")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA cache_size=-64000")
    cursor.close()