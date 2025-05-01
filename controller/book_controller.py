"""
controller/book_controller.py
-----------------------------
Handles the business logic for book records.

Provides functions for creating, editing, deleting, and searching books.
Each function returns a tuple of status and result (or error message).
All operations are logged using the centralized Logger.
"""

from typing import Tuple, Union, List
from model.entity import Book, Logger
from model.da import DataAccess


def add_book(title: str, author: str, pages: int) -> Tuple[bool, Union[Book, str]]:
    """
    Create and save a new book in the database.

    Args:
        title (str): Title of the book.
        author (str): Author of the book.
        pages (int): Number of pages.

    Returns:
        Tuple[bool, Union[Book, str]]: (True, Book instance) on success,
                                       (False, error message) on failure.
    """
    try:
        new_book = Book(title=title, author=author, pages=pages)
        DataAccess(Book).save(new_book)
        Logger.info(f"Book {new_book} saved.")
        return True, new_book
    except Exception as e:
        Logger.error(f"{e} - Book not saved.")
        return False, str(e)


def edit_book(
    id: int, title: str, author: str, pages: int
) -> Tuple[bool, Union[Book, str]]:
    """
    Update an existing book's information.

    Args:
        id (int): ID of the book to update.
        title (str): New title.
        author (str): New author.
        pages (int): New page count.

    Returns:
        Tuple[bool, Union[Book, str]]: (True, updated Book) or (False, error message).
    """
    try:
        book = Book(title=title, author=author, pages=pages)
        book.id = id
        DataAccess(Book).edit(book)
        Logger.info(f"Book {book} edited.")
        return True, book
    except Exception as e:
        Logger.error(f"{e} - Book not edited.")
        return False, str(e)


def remove_book_by_id(id: int) -> Tuple[bool, Union[Book, str]]:
    """
    Remove a book from the database by its ID.

    Args:
        id (int): ID of the book to remove.

    Returns:
        Tuple[bool, Union[Book, str]]: (True, removed Book) or (False, error message).
    """
    try:
        book_dao = DataAccess(Book)
        book = book_dao.find_by_id(id)
        if book:
            book_dao.remove_by_id(id)
            Logger.info(f"Book with ID {id} removed.")
            return True, book
        else:
            Logger.warning(f"No book found with ID {id}.")
            return False, f"No book found with ID {id}."
    except Exception as e:
        Logger.error(f"{e} - Failed to remove book with ID {id}.")
        return False, str(e)


def find_all_books() -> Tuple[bool, Union[List[Tuple[int, str, str, int]], str]]:
    """
    Retrieve all books from the database.

    Returns:
        Tuple[bool, Union[List of tuples or error string]]:
            (True, List of book tuples) or (False, error message).
            Each tuple format: (id, title, author, pages)
    """
    try:
        book_list = DataAccess(Book).find_all()
        result = []
        for b in book_list:
            try:
                result.append((b.id, b.title, b.author, b.pages))
            except Exception:
                result.append(("[Error]", "", "", ""))
        Logger.info(f"{len(result)} books retrieved.")
        return True, result
    except Exception as e:
        Logger.error(f"{e} - Error while retrieving all books.")
        return False, str(e)


def find_book_by_id(id: int) -> Tuple[bool, Union[Book, str]]:
    """
    Retrieve a single book by its ID.

    Args:
        id (int): ID of the book to retrieve.

    Returns:
        Tuple[bool, Union[Book, str]]: (True, Book) or (False, error message).
    """
    try:
        book = DataAccess(Book).find_by_id(id)
        if book:
            Logger.info(f"Book {book} found.")
            return True, book
        else:
            Logger.warning(f"No book found with ID {id}.")
            return False, f"No book found with ID {id}."
    except Exception as e:
        Logger.error(f"{e} - Error finding book with ID {id}.")
        return False, str(e)
