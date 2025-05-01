"""
controller/member_controller.py
-------------------------------
Handles business logic related to Member entities.

Provides CRUD operations and lookup functionality for members.
All operations are logged via a shared Logger instance.
"""

from typing import Tuple, Union, List
from model.entity import Member, Logger
from model.da import DataAccess


def add_member(name: str, family: str) -> Tuple[bool, Union[Member, str]]:
    """
    Create and save a new member.

    Args:
        name (str): Member's first name.
        family (str): Member's family name.

    Returns:
        Tuple[bool, Union[Member, str]]: (True, Member) on success,
                                         (False, error message) on failure.
    """
    try:
        new_member = Member(name=name, family=family)
        DataAccess(Member).save(new_member)
        Logger.info(f"Member {new_member} saved.")
        return True, new_member
    except Exception as e:
        Logger.error(f"{e} - Member not saved.")
        return False, str(e)


def edit_member(id: int, name: str, family: str) -> Tuple[bool, Union[Member, str]]:
    """
    Update an existing member by ID.

    Args:
        id (int): Member ID.
        name (str): Updated first name.
        family (str): Updated family name.

    Returns:
        Tuple[bool, Union[Member, str]]: (True, updated Member) or (False, error message).
    """
    try:
        updated_member = Member(name=name, family=family)
        updated_member.id = id
        DataAccess(Member).edit(updated_member)
        Logger.info(f"Member {updated_member} edited.")
        return True, updated_member
    except Exception as e:
        Logger.error(f"{e} - Member not edited.")
        return False, str(e)


def remove_member_by_id(id: int) -> Tuple[bool, Union[Member, str]]:
    """
    Delete a member by ID.

    Args:
        id (int): Member ID to remove.

    Returns:
        Tuple[bool, Union[Member, str]]: (True, removed Member) or (False, error message).
    """
    try:
        dao = DataAccess(Member)
        member = dao.find_by_id(id)
        if member:
            dao.remove_by_id(id)
            Logger.info(f"Member with ID {id} removed.")
            return True, member
        else:
            Logger.warning(f"No member found with ID {id}.")
            return False, f"No member found with ID {id}."
    except Exception as e:
        Logger.error(f"{e} - Failed to remove member with ID {id}.")
        return False, str(e)


def find_all_members() -> Tuple[bool, Union[List[Tuple[int, str, str]], str]]:
    """
    Retrieve all members from the database.

    Returns:
        Tuple[bool, Union[List[Tuple], str]]:
            (True, list of member tuples) or (False, error message).
            Each tuple is: (id, name, family)
    """
    try:
        members = DataAccess(Member).find_all()
        result = []
        for m in members:
            try:
                result.append((m.id, m.name, m.family))
            except Exception:
                result.append(("[Error]", "", ""))
        Logger.info(f"{len(result)} members retrieved.")
        return True, result
    except Exception as e:
        Logger.error(f"{e} - Error retrieving all members.")
        return False, str(e)


def find_member_by_id(id: int) -> Tuple[bool, Union[Member, str]]:
    """
    Retrieve a member by their ID.

    Args:
        id (int): Member ID to search.

    Returns:
        Tuple[bool, Union[Member, str]]: (True, Member) or (False, error message).
    """
    try:
        member = DataAccess(Member).find_by_id(id)
        if member:
            Logger.info(f"Member {member} found.")
            return True, member
        else:
            Logger.warning(f"No member found with ID {id}.")
            return False, f"No member found with ID {id}."
    except Exception as e:
        Logger.error(f"{e} - Error finding member with ID {id}.")
        return False, str(e)


def find_members_by_family(family: str) -> Tuple[bool, Union[List[Member], str]]:
    """
    Find all members with a matching family name.

    Args:
        family (str): Family name to filter by.

    Returns:
        Tuple[bool, Union[List[Member], str]]: (True, list of members) or (False, error message).
    """
    try:
        members = DataAccess(Member).find_all_by(Member._family == family)
        if members:
            Logger.info(f"{len(members)} members found with family name '{family}'.")
            return True, members
        else:
            Logger.warning(f"No members found with family name '{family}'.")
            return False, f"No members found with family name '{family}'."
    except Exception as e:
        Logger.error(f"{e} - Error finding members by family '{family}'.")
        return False, str(e)
