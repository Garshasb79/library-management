"""
Test: model/da/base_access.py
---------------------------------
Unit tests for generic CRUD operations via the DataAccess class.
"""

import pytest
from model.da.base_access import DataAccess
from model.entity import Member
from datetime import date


def test_save_and_find_by_id():
    da = DataAccess(Member)
    member = Member(name="TestSave", family="FamilySave")
    saved_member = da.save(member)

    found_member = da.find_by_id(saved_member.id)
    assert found_member is not None
    assert found_member.name == "TestSave"
    assert found_member.family == "FamilySave"


def test_edit():
    da = DataAccess(Member)
    member = Member(name="TestEdit", family="FamilyEdit")
    saved_member = da.save(member)

    saved_member.name = "EditedName"
    da.edit(saved_member)

    updated_member = da.find_by_id(saved_member.id)
    assert updated_member.name == "EditedName"


def test_remove():
    da = DataAccess(Member)
    member = Member(name="TestRemove", family="FamilyRemove")
    saved_member = da.save(member)

    da.remove(saved_member)
    deleted_member = da.find_by_id(saved_member.id)
    assert deleted_member is None


def test_remove_by_id():
    da = DataAccess(Member)
    member = Member(name="TestRemoveID", family="FamilyRemoveID")
    saved_member = da.save(member)

    da.remove_by_id(saved_member.id)
    deleted_member = da.find_by_id(saved_member.id)
    assert deleted_member is None


def test_find_all():
    da = DataAccess(Member)
    member1 = Member(name="All", family="FamAll")
    member2 = Member(name="all", family="famAll")
    da.save(member1)
    da.save(member2)

    members = da.find_all()
    assert any(m.name == "All" for m in members)
    assert any(m.name == "all" for m in members)


def test_find_all_by():
    da = DataAccess(Member)
    member = Member(name="Special", family="Finder")
    saved_member = da.save(member)

    found_members = da.find_all_by(Member._family == "Finder")
    assert any(m.name == "Special" for m in found_members)


# ------------------------------
# Run Tests (if script run directly)
# ------------------------------
if __name__ == "__main__":
    pytest.main([__file__])
