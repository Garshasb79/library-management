"""
model/entity/borrow.py
----------------------
Defines the Borrow entity class mapped to the 'borrows' table.
Includes validation for fields and ORM relationships to Member and Book.
"""

from typing import Union
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, ForeignKey
from model.entity import Base, Member, Book
from model.tools.validators import amount_validator, date_validator


class Borrow(Base):
    """
    ORM-mapped class representing a borrowing record in the system.
    Includes validated attributes and relationships to Member and Book entities.
    """

    __tablename__ = "borrows"

    _id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    _member_id: Mapped[int] = mapped_column(Integer, ForeignKey("members.id"))
    _book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    _borrow_date: Mapped[date] = mapped_column(Date)
    _return_date: Mapped[Union[date, None]] = mapped_column(Date, default=None)

    member = relationship("Member")
    book = relationship("Book")

    def __init__(self, member: Member, book: Book, borrow_date: Union[str, date]):
        """
        Initialize a new Borrow record with validated values.

        :param member: The Member who borrowed the book
        :param book: The Book being borrowed
        :param borrow_date: The date the book was borrowed
        """
        self._id = None
        if not isinstance(member, Member):
            raise AttributeError("Member must be a valid Member object!")
        self.member = member
        if not isinstance(book, Book):
            raise AttributeError("Book must be a valid Book object!")
        self.book = book
        self.borrow_date = borrow_date

    def __repr__(self) -> str:
        """
        Return a dictionary-like string representation without foreign keys.
        """
        return str(
            {
                col.name: getattr(self, col.name)
                for col in self.__table__.columns
                if not col.foreign_keys
            }
        )

    @property
    def id(self) -> int:
        """
        Get the borrow record ID.
        """
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Set the borrow record ID after validation.
        """
        self._id = amount_validator(value, "Invalid borrow id !")

    @property
    def member_id(self) -> int:
        """
        Get the ID of the associated member.
        """
        return self.member._id

    @member_id.setter
    def member_id(self, member: Member) -> None:
        """
        Set the member ID via a Member instance after validation.
        """
        self._member_id = amount_validator(member._id, "Invalid member id !")

    @property
    def book_id(self) -> int:
        """
        Get the ID of the associated book.
        """
        return self.book._id

    @book_id.setter
    def book_id(self, book: Book) -> None:
        """
        Set the book ID via a Book instance after validation.
        """
        self._book_id = amount_validator(book._id, "Invalid book id !")

    @property
    def borrow_date(self) -> date:
        """
        Get the borrow date.
        """
        return self._borrow_date

    @borrow_date.setter
    def borrow_date(self, value: Union[str, date]) -> None:
        """
        Set the borrow date after validating string or date input.
        """
        self._borrow_date = date_validator(value, "Invalid borrow date!")

    @property
    def return_date(self) -> Union[date, None]:
        """
        Get the return date, or None if not yet returned.
        """
        return self._return_date

    @return_date.setter
    def return_date(self, value: Union[str, date]) -> None:
        """
        Set the return date after validating string or date input.
        """
        self._return_date = date_validator(value, "Invalid return date!")
