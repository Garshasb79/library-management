"""
Test: model/entity/member.py
----------------------------
Unit tests for the Member entity model.
"""

import pytest
from model.entity.member import Member


def test_member_creation_valid():
    """Test creating a valid Member object."""
    member = Member(name="Alice", family="Smith")
    assert member.name == "Alice"
    assert member.family == "Smith"


def test_member_invalid_name():
    """Test creating a Member with invalid name."""
    with pytest.raises(ValueError, match="Invalid name!"):
        Member(name="", family="Smith")


def test_member_invalid_family():
    """Test creating a Member with invalid family."""
    with pytest.raises(ValueError, match="Invalid family!"):
        Member(name="Alice", family="12345")


def test_member_property_setters():
    """Test property setters for Member attributes."""
    member = Member(name="John", family="Doe")

    member.name = "Michael"
    member.family = "Johnson"

    assert member.name == "Michael"
    assert member.family == "Johnson"


if __name__ == "__main__":
    pytest.main([__file__])
