"""
model/da/session.py
-------------------
Manages SQLAlchemy sessions using a context manager.
Provides automatic handling of commits and rollbacks.

This module is meant to be reused anywhere safe and transactional access to the database is required.
"""

from contextlib import contextmanager
from sqlalchemy.orm import Session as SessionType  # Typing alias
from model.da.config import Session
from typing import Generator


@contextmanager
def get_session() -> Generator[SessionType, None, None]:
    """
    Provide a transactional scope for a database session.

    Automatically commits if successful, rolls back on exceptions,
    and ensures the session is closed in all cases.

    Usage:
    -------
    with get_session() as session:
        session.add(...)
        ...

    Yields:
        SessionType: An active SQLAlchemy session object.
    """
    session: SessionType = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
