"""
Test: controller/member_controller.py
-------------------------------------
Integration tests for member controller functionality.
"""

import pytest
from controller import member_controller as mc
from model.entity.member import Member


def test_add_and_find_member():
    """Test adding a member and finding it by ID."""
    status, member = mc.add_member("Alice", "Smith")
    assert status is True
    assert isinstance(member, Member)

    # Find member by ID
    status, found = mc.find_member_by_id(member.id)
    assert status is True
    assert found.name == "Alice"
    assert found.family == "Smith"


def test_edit_member():
    """Test editing an existing member."""
    _, member = mc.add_member("Bob", "Johnson")

    status, edited = mc.edit_member(member.id, "Robert", "Johns")
    assert status is True
    assert edited.name == "Robert"
    assert edited.family == "Johns"


def test_remove_member_by_id():
    """Test removing a member by ID."""
    _, member = mc.add_member("Charlie", "Brown")

    status, removed = mc.remove_member_by_id(member.id)
    assert status is True
    assert removed.id == member.id

    # Confirm deletion
    status, result = mc.find_member_by_id(member.id)
    assert status is False


def test_find_all_members():
    """Test retrieving all members."""
    status, members = mc.find_all_members()
    assert status is True
    assert isinstance(members, list)
    assert all(isinstance(m, Member) for m in members)


# اجرای دستی
if __name__ == "__main__":
    pytest.main([__file__])
