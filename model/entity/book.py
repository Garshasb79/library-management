"""
model/entity/book.py
-------------
Defines the Book entity class, mapped to the 'books' table.
Includes validation and type-safe access via properties.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from model.entity import Base
from model.tools.validators import title_validator, name_validator, amount_validator


class Book(Base):
    """
    SQLAlchemy model for a book in the library system.
    Each book has a title, author, and page count.
    """

    __tablename__ = "books"

    _id: Mapped[int] = mapped_column(
        "id", Integer, primary_key=True, autoincrement=True
    )
    _title: Mapped[str] = mapped_column("title", String(30))
    _author: Mapped[str] = mapped_column("author", String(30))
    _pages: Mapped[int] = mapped_column("pages", Integer)

    def __init__(self, title: str, author: str, pages: int):
        """
        Initialize a new Book object with validated fields.
        """
        self._id = None
        self.title = title
        self.author = author
        self.pages = pages

    @property
    def id(self) -> int:
        """Get book's ID."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """Set book's ID after validation."""
        self._id = amount_validator(value, "Invalid id!")

    @property
    def title(self) -> str:
        """Get book's title."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        """Set book's title after validation."""
        self._title = title_validator(value, "Invalid book title!")

    @property
    def author(self) -> str:
        """Get book's author name."""
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        """Set book's author name after validation."""
        self._author = name_validator(value, "Invalid author name!")

    @property
    def pages(self) -> int:
        """Get number of pages."""
        return self._pages

    @pages.setter
    def pages(self, value: int) -> None:
        """Set number of pages after validation."""
        self._pages = amount_validator(value, "Invalid pages number!")
