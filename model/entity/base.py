"""
model/entity/base.py
--------------------
Base Model Class

Provides shared functionality for all SQLAlchemy ORM models.
Includes __repr__ and to_tuple() for easy debugging and UI usage.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.

    - Inherits from SQLAlchemy DeclarativeBase to enable ORM mapping.
    - Implements common representation methods for consistency across models.
    """

    def __repr__(self) -> str:
        """
        Return a string representation of the model instance,
        showing all column values as a dictionary.
        """
        return str({c.name: getattr(self, c.name) for c in self.__table__.columns})

    def to_tuple(self) -> tuple:
        """
        Return all column values as a tuple (used for populating tables, etc.).
        """
        return tuple(getattr(self, c.name) for c in self.__table__.columns)
