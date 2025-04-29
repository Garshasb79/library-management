"""
Test: controller/borrow_controller.py
-------------------------------------
Integration tests for borrow controller functionality.
"""

import pytest
from controller import borrow_controller as bc
from controller import member_controller as mc
from controller import book_controller as boc
from datetime import date


def test_add_and_find_borrow():
    # Create a member and a book first
    _, member = mc.add_member("Test", "Borrower")
    _, book = boc.add_book("Borrowed Book", "Author X", 200)

    # Add borrow
    borrow_date = date.today()
    status, borrow = bc.add_borrow(member.id, book.id, borrow_date, None)
    assert status is True

    # Find borrow by ID
    status, found_borrow = bc.find_borrow_by_id(borrow.id)
    assert status is True


def test_edit_borrow():
    _, member = mc.add_member("Edit", "Borrower")
    _, book = boc.add_book("Edit Book", "Edit Author", 222)

    # Add a borrow
    borrow_date = date.today()
    status, borrow = bc.add_borrow(member.id, book.id, borrow_date, None)
    assert status is True

    # Update borrow with return_date
    return_date = date.today()
    status, edited = bc.edit_borrow(
        borrow.id, member.id, book.id, borrow_date, return_date
    )
    assert status is True
    assert edited.return_date == return_date


def test_remove_borrow_by_id():
    _, member = mc.add_member("Delete", "Borrower")
    _, book = boc.add_book("Delete Book", "Author D", 300)

    # Add and then remove borrow
    status, borrow = bc.add_borrow(member.id, book.id, date.today(), None)
    assert status is True

    status, removed = bc.remove_borrow_by_id(borrow.id)
    assert status is True

    # Confirm it’s removed
    status, result = bc.find_borrow_by_id(borrow.id)
    assert status is False


# اجرای دستی
if __name__ == "__main__":
    pytest.main([__file__])
