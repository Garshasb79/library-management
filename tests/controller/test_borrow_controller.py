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
    _, member = mc.add_member("Test", "Borrower")
    _, book = boc.add_book("Borrowed Book", "Author X", 200)
    borrow_date = date.today()
    status, borrow = bc.add_borrow(member.id, book.id, borrow_date, None)
    assert status is True
    status, found_borrow = bc.find_borrow_by_id(borrow.id)
    assert status is True


def test_edit_borrow():
    _, member = mc.add_member("Edit", "Borrower")
    _, book = boc.add_book("Edit Book", "Edit Author", 222)
    borrow_date = date.today()
    status, borrow = bc.add_borrow(member.id, book.id, borrow_date, None)
    assert status is True
    return_date = date.today()
    status, edited = bc.edit_borrow(
        borrow.id, member.id, book.id, borrow_date, return_date
    )
    assert status is True
    assert edited.return_date == return_date


def test_remove_borrow_by_id():
    _, member = mc.add_member("Delete", "Borrower")
    _, book = boc.add_book("Delete Book", "Author D", 300)
    status, borrow = bc.add_borrow(member.id, book.id, date.today(), None)
    assert status is True
    status, removed = bc.remove_borrow_by_id(borrow.id)
    assert status is True
    status, result = bc.find_borrow_by_id(borrow.id)
    assert status is False


def test_find_all_borrows():
    _, member = mc.add_member("All", "Borrows")
    _, book = boc.add_book("AllBook", "Author All", 111)
    bc.add_borrow(member.id, book.id, date.today(), None)

    status, result = bc.find_all_borrows()
    assert status is True
    assert isinstance(result, list)
    assert any(row[1] == member.id and row[2] == book.id for row in result)


if __name__ == "__main__":
    pytest.main([__file__])
