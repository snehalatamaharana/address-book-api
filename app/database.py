"""SQLite database configuration."""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./address_book.db"

# check_same_thread=False is required for SQLite when used with FastAPI
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base class for all ORM models."""


def get_db():
    """Yield a DB session per request and always close it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()