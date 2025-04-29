"""
controller/report_controller.py
-------------------------------
Provides high-level data preparation for reporting purposes.

Each function returns a structured list of tuples, formatted and ready to be consumed by the UI layer (Treeview).

Reports include:
- Books currently borrowed
- Books never borrowed
- Members with unreturned books
- Members who never borrowed
- All borrow records
- Borrow count per book
"""

from typing import List, Tuple
from datetime import date
from model.da.session import get_session
from model.da.reports import *


def get_currently_borrowed_info() -> List[Tuple]:
    """
    Retrieve a list of currently borrowed books with borrower details.

    :return: List of tuples → (book_id, title, member_id, first_name, last_name, borrow_date)
    """
    with get_session() as session:
        borrows = get_current_borrows_with_details(session)
        data = []

        for b in borrows:
            try:
                data.append(
                    (
                        b.book.id,
                        b.book.title,
                        b.member.id,
                        b.member.name,
                        b.member.family,
                        b.borrow_date.strftime("%Y-%m-%d") if b.borrow_date else "-",
                    )
                )
            except Exception:
                data.append(("[Error]", "", "", "", "", ""))
        return data


def get_books_never_borrowed_info() -> List[Tuple]:
    """
    Retrieve books that have never been borrowed.

    :return: List of tuples → (book_id, title, author)
    """
    with get_session() as session:
        books = get_books_never_borrowed(session)
        data = []

        for book in books:
            try:
                data.append((book.id, book.title, book.author))
            except Exception:
                data.append(("[Error]", "", ""))
        return data


def get_members_with_unreturned_info() -> List[Tuple]:
    """
    Get members who have unreturned books and the delay in days.

    :return: List of tuples → (member_id, first_name, last_name, book_title, delay_days)
    """
    with get_session() as session:
        borrows = get_members_with_unreturned_books(session)
        data = []
        today = date.today()

        for b in borrows:
            try:
                delay = (today - b.borrow_date).days
                data.append(
                    (b.member.id, b.member.name, b.member.family, b.book.title, delay)
                )
            except Exception:
                data.append(("[Error]", "", "", "", ""))
        return data


def get_members_never_borrowed_info() -> List[Tuple]:
    """
    Get members who have never borrowed a book.

    :return: List of tuples → (member_id, first_name, last_name)
    """
    with get_session() as session:
        members = get_members_never_borrowed(session)
        data = []

        for m in members:
            try:
                data.append((m.id, m.name, m.family))
            except Exception:
                data.append(("[Error]", "", ""))
        return data


def get_report_all_borrows_info() -> List[Tuple]:
    """
    Retrieve all borrow records with member and book info.

    :return: List of tuples → (member_id, first_name, last_name, book_id, title, author, borrow_date, return_date)
    """
    with get_session() as session:
        borrows = get_report_all_borrows(session)
        data = []

        for b in borrows:
            try:
                data.append(
                    (
                        b.member.id,
                        b.member.name,
                        b.member.family,
                        b.book.id,
                        b.book.title,
                        b.book.author,
                        b.borrow_date,
                        b.return_date,
                    )
                )
            except Exception:
                data.append(("[Error]", "", "", "", "", "", "", ""))
        return data


def get_book_borrow_counts_info() -> List[Tuple]:
    """
    Get a list of books along with the number of times they were borrowed.

    :return: List of tuples → (book_id, title, author, borrow_count)
    """
    with get_session() as session:
        results = get_book_borrow_counts(session)
        data = []

        for row in results:
            try:
                data.append((row[0], row[1], row[2], row[3]))
            except Exception:
                data.append(("[Error]", "", "", ""))
        return data
