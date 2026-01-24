from sqlalchemy import create_engine
from core.system.config import DATABASE_PATH


engine = create_engine(
    DATABASE_PATH,
    echo=False
)