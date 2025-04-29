"""
Test: model/entity/borrow.py
-----------------------------
Unit tests for Borrow entity class.
"""

import pytest
from model.entity import Member, Book, Borrow
from datetime import date


def test_borrow_creation_valid():
    """Test creating a valid Borrow record."""
    member = Member(name="John", family="Doe")
    book = Book(title="Test Book", author="Author Name", pages=123)
    borrow_date = date.today()

    borrow = Borrow(member, book, borrow_date)

    assert borrow.member == member
    assert borrow.book == book
    assert borrow.borrow_date == borrow_date
    assert borrow.return_date is None


def test_borrow_with_return_date():
    """Test creating a Borrow record with a return date."""
    member = Member(name="Anna", family="Smith")
    book = Book(title="Another Book", author="Another Author", pages=321)
    borrow_date = date.today()
    return_date = date.today()

    borrow = Borrow(member, book, borrow_date)
    borrow.return_date = return_date

    assert borrow.return_date == return_date


def test_borrow_invalid_member():
    """Test Borrow creation with invalid member object."""
    book = Book(title="Some Book", author="Author", pages=100)
    with pytest.raises(AttributeError):
        Borrow(None, book, date.today())


def test_borrow_invalid_book():
    """Test Borrow creation with invalid book object."""
    member = Member(name="James", family="Bond")
    with pytest.raises(AttributeError):
        Borrow(member, None, date.today())


def test_borrow_invalid_borrow_date():
    """Test Borrow creation with invalid borrow date."""
    member = Member(name="Bruce", family="Wayne")
    book = Book(title="Dark Knight", author="Gotham Writer", pages=250)
    with pytest.raises(ValueError):
        Borrow(member, book, "invalid-date")


if __name__ == "__main__":
    import pytest

    pytest.main()
