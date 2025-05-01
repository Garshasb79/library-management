"""
Test: controller/book_controller.py
------------------------------------
Integration tests for book controller functionality.
"""

import pytest
from controller import book_controller as bc
from model.entity.book import Book


def test_add_and_find_book():
    """Test adding a book and retrieving it."""
    status, book = bc.add_book(title="Python 101", author="Michael", pages=300)
    assert status is True
    assert isinstance(book, Book)
    assert book.title == "Python 101"
    assert book.author == "Michael"
    assert book.pages == 300

    # Now find it
    status, found = bc.find_book_by_id(book.id)
    assert status is True
    assert found.id == book.id


def test_edit_book():
    """Test editing an existing book."""
    status, book = bc.add_book(title="Old Title", author="Old Author", pages=200)
    assert status is True

    # Edit it
    new_title = "New Title"
    new_author = "New Author"
    new_pages = 250
    status, edited = bc.edit_book(book.id, new_title, new_author, new_pages)
    assert status is True
    assert edited.title == new_title
    assert edited.author == new_author
    assert edited.pages == new_pages


def test_remove_book_by_id():
    """Test removing a book by ID."""
    status, book = bc.add_book(title="Temp Book", author="Someone", pages=150)
    assert status is True

    status, removed = bc.remove_book_by_id(book.id)
    assert status is True
    assert removed.id == book.id

    # Make sure it is removed
    status, found = bc.find_book_by_id(book.id)
    assert status is False


# اجرای دستی
if __name__ == "__main__":
    pytest.main([__file__])
