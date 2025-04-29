"""
Test: model/da/reports.py
-------------------------
Integration tests for report queries and summaries.
"""

import pytest
from model.da.session import get_session
from model.da.reports import (
    get_current_borrows_with_details,
    get_books_never_borrowed,
    get_members_with_unreturned_books,
    get_report_all_borrows,
    get_members_never_borrowed,
    get_book_borrow_counts,
)
from model.entity.borrow import Borrow
from model.entity.book import Book
from model.entity.member import Member


def test_get_current_borrows_with_details():
    with get_session() as session:
        results = get_current_borrows_with_details(session)
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, Borrow)
            assert item.book is not None
            assert item.member is not None


def test_get_books_never_borrowed():
    with get_session() as session:
        results = get_books_never_borrowed(session)
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, Book)


def test_get_members_with_unreturned_books():
    with get_session() as session:
        results = get_members_with_unreturned_books(session)
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, Borrow)
            assert item.book is not None
            assert item.member is not None


def test_get_report_all_borrows():
    with get_session() as session:
        results = get_report_all_borrows(session)
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, Borrow)
            assert item.book is not None
            assert item.member is not None


def test_get_members_never_borrowed():
    with get_session() as session:
        results = get_members_never_borrowed(session)
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, Member)


def test_get_book_borrow_counts():
    with get_session() as session:
        results = get_book_borrow_counts(session)
        assert isinstance(results, list)
        for row in results:
            assert isinstance(row, tuple)
            assert len(row) == 4  # (book_id, title, author, borrow_count)


# برای اجرای دستی
if __name__ == "__main__":
    pytest.main([__file__])
