"""
Test: model/entity/book.py
---------------------------
Unit tests for the Book entity class.
"""

import pytest
from model.entity.book import Book


def test_book_creation_valid():
    book = Book(title="Effective Python", author="Brett Slatkin", pages=250)
    assert book.title == "Effective Python"
    assert book.author == "Brett Slatkin"
    assert book.pages == 250


def test_book_invalid_title():
    with pytest.raises(ValueError):
        Book(title="", author="Author", pages=123)


def test_book_invalid_author():
    with pytest.raises(ValueError):
        Book(title="Book Title", author="", pages=123)


def test_book_invalid_pages():
    with pytest.raises(ValueError):
        Book(title="Book Title", author="Author", pages=-10)


def test_book_property_setters():
    book = Book(title="Clean Code", author="Robert C. Martin", pages=464)
    book.title = "The Pragmatic Programmer"
    book.author = "Andrew Hunt"
    book.pages = 320

    assert book.title == "The Pragmatic Programmer"
    assert book.author == "Andrew Hunt"
    assert book.pages == 320


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", __file__])
