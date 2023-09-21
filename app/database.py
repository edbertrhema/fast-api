from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pymysql # Importing pymysql
from .config import settings

MYSQL_DATABASE_URL = f'mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}?charset=utf8mb4'

engine = create_engine(MYSQL_DATABASE_URL)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()