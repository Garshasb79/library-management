"""
controller/borrow_controller.py
-------------------------------
Handles the business logic for borrowing records.

This module provides functions to create, edit, delete, and retrieve
borrow records. It ensures proper validation and interaction between
members, books, and borrow entries. Logging is performed for all actions.
"""

from typing import Tuple, Union, List
from datetime import date
from model.entity import Member, Book, Borrow, Logger
from model.da import DataAccess
from model.da.session import get_session
from sqlalchemy.orm import joinedload


def add_borrow(
    member_id: int, book_id: int, borrow_date: date, return_date: Union[date, None]
) -> Tuple[bool, Union[Borrow, str]]:
    """
    Create and save a new borrow record.

    Args:
        member_id (int): ID of the borrowing member.
        book_id (int): ID of the borrowed book.
        borrow_date (date): Date of borrowing.
        return_date (date | None): Optional return date.

    Returns:
        Tuple[bool, Borrow or error message].
    """
    try:
        member = DataAccess(Member).find_by_id(member_id)
        book = DataAccess(Book).find_by_id(book_id)
        new_borrow = Borrow(member, book, borrow_date)
        if return_date is not None:
            new_borrow.return_date = return_date

        DataAccess(Borrow).save(new_borrow)
        Logger.info(f"Borrow {new_borrow} saved.")
        return True, new_borrow
    except Exception as e:
        Logger.error(f"{e} - Borrow not saved.")
        return False, str(e)


def edit_borrow(
    id: int,
    member_id: int,
    book_id: int,
    borrow_date: date,
    return_date: Union[date, None]
) -> Tuple[bool, Union[Borrow, str]]:
    """
    Edit an existing borrow record.

    Args:
        id (int): ID of the borrow to update.
        member_id (int): Updated member ID.
        book_id (int): Updated book ID.
        borrow_date (date): Updated borrow date.
        return_date (date | None): Optional return date.

    Returns:
        Tuple[bool, Borrow or error message].
    """
    try:
        member = DataAccess(Member).find_by_id(member_id)
        book = DataAccess(Book).find_by_id(book_id)
        updated_borrow = Borrow(member, book, borrow_date)
        updated_borrow.id = id
        if return_date:
            updated_borrow.return_date = return_date

        DataAccess(Borrow).edit(updated_borrow)
        Logger.info(f"Borrow {updated_borrow} edited.")
        return True, updated_borrow
    except Exception as e:
        Logger.error(f"{e} - Borrow not edited.")
        return False, str(e)


def remove_borrow_by_id(id: int) -> Tuple[bool, Union[Borrow, str]]:
    """
    Delete a borrow record by ID.

    Args:
        id (int): ID of the borrow to delete.

    Returns:
        Tuple[bool, Borrow or error message].
    """
    try:
        dao = DataAccess(Borrow)
        borrow = dao.find_by_id(id)
        if borrow:
            dao.remove_by_id(id)
            Logger.info(f"Borrow with ID {id} removed.")
            return True, borrow
        else:
            Logger.warning(f"No borrow found with ID {id}.")
            return False, f"No borrow found with ID {id}."
    except Exception as e:
        Logger.error(f"{e} - Failed to remove borrow with ID {id}.")
        return False, str(e)


def find_all_borrows() -> Tuple[bool, Union[List[Tuple[int, int, int, date, Union[date, None]]], str]]:
    """
    Retrieve all borrow records, with member and book details loaded.

    Returns:
        Tuple[bool, List of borrow tuples or error string].
        Each tuple contains: (borrow_id, member_id, book_id, borrow_date, return_date)
    """
    try:
        with get_session() as session:
            borrows = (
                session.query(Borrow)
                .options(joinedload(Borrow.member), joinedload(Borrow.book))
                .all()
            )

            data = []
            for b in borrows:
                try:
                    data.append(
                        (b.id, b.member.id, b.book.id, b.borrow_date, b.return_date)
                    )
                except Exception:
                    data.append(("[Error]", "", "", "", ""))

            Logger.info(f"{len(data)} borrows retrieved.")
            return True, data
    except Exception as e:
        Logger.error(f"{e} - Error retrieving borrows.")
        return False, str(e)


def find_borrow_by_id(id: int) -> Tuple[bool, Union[Borrow, str]]:
    """
    Retrieve a single borrow record by ID.

    Args:
        id (int): ID of the borrow record.

    Returns:
        Tuple[bool, Borrow or error message].
    """
    try:
        borrow = DataAccess(Borrow).find_by_id(id)
        if borrow:
            Logger.info(f"Borrow {borrow} found.")
            return True, borrow
        else:
            Logger.warning(f"No borrow found with ID {id}.")
            return False, f"No borrow found with ID {id}."
    except Exception as e:
        Logger.error(f"{e} - Borrow not found.")
        return False, str(e)
