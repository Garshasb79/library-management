"""
controller/book_controller.py
----------------------------
Handles the business logic for book records. Provides
functions for creating, editing, deleting, and searching
books. Uses the Logger for operation tracking.
"""

from typing import Tuple, Union, List
import traceback
from model.entity import Book, Logger
from model.da import DataAccess


def add_book(title: str, author: str, pages: int) -> Tuple[bool, Union[Book, str]]:
    """Create and save a new book."""
    try:
        new_book = Book(title=title, author=author, pages=pages)
        book_da = DataAccess(Book)
        book_da.save(new_book)
        Logger.info(f"Book {new_book} saved.")
        return True, new_book
    except Exception as e:
        Logger.error(f"{e} Not saved.")
        return False, str(e)


def edit_book(
    id: int, title: str, author: str, pages: int
) -> Tuple[bool, Union[Book, str]]:
    """Edit an existing book."""
    try:
        new_book = Book(title=title, author=author, pages=pages)
        new_book.id = id
        book_da = DataAccess(Book)
        book_da.edit(new_book)
        Logger.info(f"Book {new_book} edited.")
        return True, new_book
    except Exception as e:
        Logger.error(f"{e} Not edited.")
        return False, str(e)


def remove_book_by_id(id: int) -> Tuple[bool, Union[Book, str]]:
    """Remove a book by its ID."""
    try:
        book_da = DataAccess(Book)
        book = book_da.find_by_id(id)
        if book:
            book_da.remove_by_id(id)
            Logger.info(f"Book by id {id} removed.")
            return True, book
        else:
            Logger.warning(f"No book by id {id} found.")
            return False, f"No book by id {id} found."
    except Exception as e:
        traceback.print_exc()
        Logger.error(f"{e} Book by id {id} not removed.")
        return False, str(e)


def find_all_books() -> Tuple[bool, Union[List[Book], str]]:
    """Retrieve all books from the database."""
    try:
        book_da = DataAccess(Book)
        book_list = book_da.find_all()
        Logger.info(f"{len(book_list)} books found.")
        return True, book_list
    except Exception as e:
        Logger.error(f"{e} While finding all books.")
        return False, str(e)


def find_book_by_id(id: int) -> Tuple[bool, Union[Book, str]]:
    """Retrieve a single book by ID."""
    try:
        book_da = DataAccess(Book)
        book = book_da.find_by_id(id)
        if book:
            Logger.info(f"Book {book} found.")
            return True, book
        else:
            Logger.warning(f"No book by id {id} found.")
            return False, f"No book by id {id} found."
    except Exception as e:
        Logger.error(f"{e} Book {id} not found.")
        return False, str(e)
