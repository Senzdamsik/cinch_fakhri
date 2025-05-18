from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Get a database session.

    Yields:
        Session: A SQLAlchemy database session.

    Note:
        This function is intended to be used as a FastAPI dependency.
        The session is automatically closed when the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
