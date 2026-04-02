from sqlalchemy.orm import sessionmaker
from core.db.engine import engine


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

SessionLocalCash = sessionmaker(bind=engine, expire_on_commit=True)