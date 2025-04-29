"""
model/da/reports.py
-------------------
Provides report-specific queries and analytics for the application.
This module retrieves custom data patterns and summaries using SQLAlchemy ORM.

Functions:
- get_current_borrows_with_details
- get_books_never_borrowed
- get_members_with_unreturned_books
- get_report_all_borrows
- get_members_never_borrowed
- get_book_borrow_counts
"""

from typing import List, Tuple
from sqlalchemy import func, exists
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from model.entity.book import Book
from model.entity.member import Member
from model.entity.borrow import Borrow


def get_current_borrows_with_details(session: Session) -> List[Borrow]:
    """
    Retrieve currently borrowed records with related book and member details.

    Args:
        session: SQLAlchemy session object.

    Returns:
        List of Borrow ORM objects.
    """
    return (
        session.query(Borrow)
        .options(joinedload(Borrow.book), joinedload(Borrow.member))
        .filter(Borrow._return_date.is_(None))
        .all()
    )


def get_books_never_borrowed(session: Session) -> List[Book]:
    """
    Retrieve books that have never been borrowed.

    Args:
        session: SQLAlchemy session object.

    Returns:
        List of Book ORM objects.
    """
    borrowed_book_ids = session.query(Borrow._book_id).distinct()
    return session.query(Book).filter(Book._id.not_in(borrowed_book_ids)).all()


def get_members_with_unreturned_books(session: Session) -> List[Borrow]:
    """
    Retrieve borrows where books have not been returned yet.

    Args:
        session: SQLAlchemy session object.

    Returns:
        List of Borrow ORM objects.
    """
    return (
        session.query(Borrow)
        .options(joinedload(Borrow.member), joinedload(Borrow.book))
        .filter(Borrow._return_date.is_(None))
        .all()
    )


def get_report_all_borrows(session: Session) -> List[Borrow]:
    """
    Retrieve all borrow records with full member and book details.

    Args:
        session: SQLAlchemy session object.

    Returns:
        List of Borrow ORM objects.
    """
    return (
        session.query(Borrow)
        .options(joinedload(Borrow.member), joinedload(Borrow.book))
        .all()
    )


def get_members_never_borrowed(session: Session) -> List[Member]:
    """
    Retrieve members who have never borrowed any books.

    Args:
        session: SQLAlchemy session object.

    Returns:
        List of Member ORM objects.
    """
    return (
        session.query(Member)
        .filter(~exists().where(Member._id == Borrow._member_id))
        .all()
    )


def get_book_borrow_counts(session: Session) -> List[Tuple[int, str, str, int]]:
    """
    Returns a list of books with the number of times each has been borrowed.

    :param session: SQLAlchemy session object
    :return: List of tuples: (book_id, title, author, borrow_times)
    """
    results = (
        session.query(
            Book._id,
            Book._title,
            Book._author,
            func.count(Borrow._book_id).label("borrow_times"),
        )
        .join(Borrow, Borrow._book_id == Book._id)
        .group_by(Book._id, Book._title, Book._author)
        .order_by(func.count(Borrow._book_id).desc())
        .all()
    )
    return [tuple(row) for row in results]
