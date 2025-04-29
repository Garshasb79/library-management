"""
Test: controller/report_controller.py
--------------------------------------
Integration tests for report controller functionality.
"""

import pytest
from controller import report_controller as rc
from controller import member_controller as mc
from controller import book_controller as boc
from controller import borrow_controller as bc
from datetime import date


def test_get_currently_borrowed_info():
    """Test retrieving currently borrowed books."""
    # آماده‌سازی داده‌ها
    _, member = mc.add_member("Borrower", "User")
    _, book = boc.add_book("Borrowed Book", "Author B", 150)
    bc.add_borrow(member.id, book.id, date.today(), None)

    data = rc.get_currently_borrowed_info()
    assert isinstance(data, list)
    assert any(row[1] == "Borrowed Book" for row in data)


def test_get_books_never_borrowed_info():
    """Test retrieving books never borrowed."""
    _, book = boc.add_book("NeverBorrowed", "Author N", 120)

    data = rc.get_books_never_borrowed_info()
    assert isinstance(data, list)
    assert any(row[1] == "NeverBorrowed" for row in data)


def test_get_members_with_unreturned_info():
    """Test retrieving members with unreturned books."""
    _, member = mc.add_member("Late", "Returner")
    _, book = boc.add_book("Late Book", "Author L", 100)
    bc.add_borrow(member.id, book.id, date.today(), None)

    data = rc.get_members_with_unreturned_info()
    assert isinstance(data, list)
    assert any(row[1] == "Late" for row in data)


def test_get_members_never_borrowed_info():
    """Test retrieving members who never borrowed any book."""
    _, member = mc.add_member("No", "Borrow")

    data = rc.get_members_never_borrowed_info()
    assert isinstance(data, list)
    assert any(row[1] == "No" for row in data)


def test_get_report_all_borrows_info():
    """Test retrieving full borrow report."""
    data = rc.get_report_all_borrows_info()
    assert isinstance(data, list)


def test_get_book_borrow_counts_info():
    """Test retrieving count of borrows per book."""
    data = rc.get_book_borrow_counts_info()
    assert isinstance(data, list)
    for row in data:
        assert isinstance(row, tuple)
        assert len(row) == 4


# اجرای دستی
if __name__ == "__main__":
    pytest.main([__file__])
