"""
controller/member_controller.py
------------------------------
Handles all business logic related to Member entities.
Provides CRUD operations and member lookup utilities.
Logs operations using the shared Logger.
"""

from typing import Tuple, Union
from model.entity import Member, Logger
from model.da import DataAccess


def add_member(name: str, family: str) -> Tuple[bool, Union[Member, str]]:
    """Create and save a new member."""
    try:
        new_member = Member(name=name, family=family)
        member_da = DataAccess(Member)
        member_da.save(new_member)
        Logger.info(f"Member {new_member} saved.")
        return True, new_member
    except Exception as e:
        Logger.error(f"{e} Not saved.")
        return False, str(e)


def edit_member(id: int, name: str, family: str) -> Tuple[bool, Union[Member, str]]:
    """Update an existing member by ID."""
    try:
        new_member = Member(name=name, family=family)
        new_member.id = id
        member_da = DataAccess(Member)
        member_da.edit(new_member)
        Logger.info(f"Member {new_member} edited.")
        return True, new_member
    except Exception as e:
        Logger.error(f"{e} Not edited.")
        return False, str(e)


def remove_member_by_id(id: int) -> Tuple[bool, Union[Member, str]]:
    """Remove a member from the database by ID."""
    try:
        member_da = DataAccess(Member)
        member = member_da.find_by_id(id)
        if member:
            member_da.remove_by_id(id)
            Logger.info(f"Member by id {id} removed.")
            return True, member
        else:
            Logger.warning(f"No member by id {id} found.")
            return False, f"No member by id {id} found."
    except Exception as e:
        Logger.error(f"{e} Member by id {id} not removed.")
        return False, str(e)


def find_all_members() -> Tuple[bool, Union[list, str]]:
    """Retrieve all members from the database."""
    try:
        member_da = DataAccess(Member)
        member_list = member_da.find_all()
        Logger.info(f"{len(member_list)} members found.")
        return True, member_list
    except Exception as e:
        Logger.error(f"{e} While finding all members.")
        return False, str(e)


def find_member_by_id(id: int) -> Tuple[bool, Union[Member, str]]:
    """Find a member by their ID."""
    try:
        member_da = DataAccess(Member)
        member = member_da.find_by_id(id)
        if member:
            Logger.info(f"Member {member} found.")
            return True, member
        else:
            Logger.warning(f"No member by id {id} found.")
            return False, f"No member by id {id} found."
    except Exception as e:
        Logger.error(f"{e} Member {id} not found.")
        return False, str(e)


def find_members_by_family(family: str) -> Tuple[bool, Union[list, str]]:
    """Find all members by their family name."""
    try:
        member_da = DataAccess(Member)
        members = member_da.find_all_by(Member._family == family)
        if members:
            Logger.info(f"{len(members)} member/s {members} found by {family}.")
            return True, members
        else:
            Logger.warning(f"No member by family {family} found.")
            return False, f"No member by family {family} found."
    except Exception as e:
        Logger.error(f"{e} Member {family} not found.")
        return False, str(e)
