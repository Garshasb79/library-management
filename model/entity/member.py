"""
model/entity/member.py
---------------
Defines the Member entity class, mapped to the 'members' table.
Includes field validation and type-safe access via properties.
"""

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from model.entity import Base
from model.tools.validators import name_validator, amount_validator


class Member(Base):
    """
    SQLAlchemy model for a library member.
    Represents a row in the 'members' table.
    Includes validation on set operations via property setters.
    """

    __tablename__ = "members"

    _id: Mapped[int] = mapped_column(
        "id", Integer, primary_key=True, autoincrement=True
    )
    _name: Mapped[str] = mapped_column("name", String(30))
    _family: Mapped[str] = mapped_column("family", String(30))

    def __init__(self, name: str, family: str):
        """
        Initialize a new Member object with validated fields.
        """
        self._id = None
        self.name = name
        self.family = family

    @property
    def id(self) -> int:
        """Get member's ID."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """Set member's ID after validation."""
        self._id = amount_validator(value, "Invalid id!")

    @property
    def name(self) -> str:
        """Get member's name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set member's name after validation."""
        self._name = name_validator(value, "Invalid name!")

    @property
    def family(self) -> str:
        """Get member's family name."""
        return self._family

    @family.setter
    def family(self, value: str) -> None:
        """Set member's family name after validation."""
        self._family = name_validator(value, "Invalid family!")
