from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import get_settings

SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False )
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db   
    finally:   
        db.close()