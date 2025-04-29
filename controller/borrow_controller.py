""" 
controller/borrow_controller.py
-------------------------------
Handles the business logic for borrowing records. Provides
functions for creating, editing, deleting, and searching
borrows. Uses the Logger for operation tracking.
"""

from typing import Tuple, Union, List
from model.entity import Member, Book, Borrow, Logger
from model.da import DataAccess
from model.da.session import get_session
from sqlalchemy.orm import joinedload


def add_borrow(
    member_id: int, book_id: int, borrow_date, return_date
) -> Tuple[bool, Union[Borrow, str]]:
    """Create and save a new borrow record."""
    try:
        member_da = DataAccess(Member)
        member = member_da.find_by_id(member_id)
        book_da = DataAccess(Book)
        book = book_da.find_by_id(book_id)
        new_borrow = Borrow(member, book, borrow_date)
        if return_date is not None:
            new_borrow.return_date = return_date
        borrow_da = DataAccess(Borrow)
        borrow_da.save(new_borrow)
        Logger.info(f"Borrow {new_borrow} saved.")
        return True, new_borrow
    except Exception as e:
        Logger.error(f"{e} Not saved.")
        return False, str(e)


def edit_borrow(
    id: int, member_id: int, book_id: int, borrow_date, return_date
) -> Tuple[bool, Union[Borrow, str]]:
    """Edit an existing borrow record."""
    try:
        member_da = DataAccess(Member)
        member = member_da.find_by_id(member_id)
        book_da = DataAccess(Book)
        book = book_da.find_by_id(book_id)
        new_borrow = Borrow(member, book, borrow_date)
        if return_date and return_date != "None":
            new_borrow.return_date = return_date
        new_borrow.id = id
        borrow_da = DataAccess(Borrow)
        borrow_da.edit(new_borrow)
        Logger.info(f"Borrow {new_borrow} edited.")
        return True, new_borrow
    except Exception as e:
        Logger.error(f"{e} Not edited.")
        return False, str(e)


def remove_borrow_by_id(id: int) -> Tuple[bool, Union[Borrow, str]]:
    """Delete a borrow record by ID."""
    try:
        borrow_da = DataAccess(Borrow)
        borrow = borrow_da.find_by_id(id)
        if borrow:
            borrow_da.remove_by_id(id)
            Logger.info(f"Borrow by id {id} removed.")
            return True, borrow
        else:
            Logger.warning(f"No borrow by id {id} found.")
            return False, f"No borrow by id {id} found."
    except Exception as e:
        Logger.error(f"{e} Borrow by id {id} not removed.")
        return False, str(e)


def find_all_borrows() -> Tuple[bool, Union[List[Borrow], str]]:
    """Retrieve all borrow records."""
    try:
        borrow_da = DataAccess(Borrow)
        borrow_list = borrow_da.find_all()
        Logger.info(f"{len(borrow_list)} borrows found.")
        return True, borrow_list
    except Exception as e:
        Logger.error(f"{e} While finding all borrows.")
        return False, str(e)


def find_borrow_by_id(id: int) -> Tuple[bool, Union[Borrow, str]]:
    """Retrieve a single borrow by ID."""
    try:
        borrow_da = DataAccess(Borrow)
        borrow = borrow_da.find_by_id(id)
        if borrow:
            Logger.info(f"Borrow {borrow} found.")
            return True, borrow
        else:
            Logger.warning(f"No borrow by id {id} found.")
            return False, f"No borrow by id {id} found."
    except Exception as e:
        Logger.error(f"{e} Borrow {id} not found.")
        return False, str(e)


def find_by_member_id(member_id: int) -> Tuple[bool, Union[List[Borrow], str]]:
    """Find all borrow records by member ID."""
    try:
        borrow_da = DataAccess(Borrow)
        borrows = borrow_da.find_all_by(Borrow.member_id == member_id)
        if borrows:
            Logger.info(f"{len(borrows)} borrow/s found by id {member_id}.")
            return True, borrows
        else:
            Logger.warning(f"No member by id {member_id} found.")
            return False, f"No member by id {member_id} found."
    except Exception as e:
        Logger.error(f"{e} Borrow for id {member_id} not found.")
        return False, str(e)


def find_by_book_id(book_id: int) -> Tuple[bool, Union[List[Borrow], str]]:
    """Find all borrow records by book ID."""
    try:
        borrow_da = DataAccess(Borrow)
        borrows = borrow_da.find_all_by(Borrow.book_id == book_id)
        if borrows:
            Logger.info(f"{len(borrows)} borrow/s found by id {book_id}.")
            return True, borrows
        else:
            Logger.warning(f"No book by id {book_id} found.")
            return False, f"No book by id {book_id} found."
    except Exception as e:
        Logger.error(f"{e} Borrow for id {book_id} not found.")
        return False, str(e)
