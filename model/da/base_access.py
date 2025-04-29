"""
model/da/base_access.py
-----------------------
Provides generic CRUD operations for any entity model.
Uses context-managed database sessions for safe and transactional access.
"""

from typing import Type, List, Optional, Any
from model.da.session import get_session


class DataAccess:
    """
    Generic Data Access Object (DAO) for performing CRUD operations.

    Attributes:
        class_name (Type): SQLAlchemy model class to operate on.
    """

    def __init__(self, class_name: Type) -> None:
        self.class_name = class_name

    def save(self, entity: Any) -> Any:
        """Add a new entity to the database and return it after refresh."""
        with get_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            session.expunge(entity)
            return entity

    def edit(self, entity: Any) -> Any:
        """Update an existing entity using SQLAlchemy's merge."""
        with get_session() as session:
            session.merge(entity)
            return entity

    def remove(self, entity: Any) -> Optional[Any]:
        """Delete an entity using its reference."""
        with get_session() as session:
            found = session.get(self.class_name, entity.id)
            if found:
                session.delete(found)
                session.commit()
                return found
        return None

    def remove_by_id(self, entity_id: int) -> Optional[Any]:
        """Delete an entity by its ID."""
        with get_session() as session:
            found = session.get(self.class_name, entity_id)
            if found:
                session.delete(found)
                session.commit()
                return found
        return None

    def find_all(self) -> List[Any]:
        """Return all instances of the entity from the database."""
        with get_session() as session:
            entities = session.query(self.class_name).all()
            for entity in entities:
                session.expunge(entity)
            return entities

    def find_by_id(self, id: int) -> Optional[Any]:
        """Find a single entity by ID."""
        with get_session() as session:
            entity = session.get(self.class_name, id)
            if entity:
                session.expunge(entity)
            return entity

    def find_all_by(self, condition: Any) -> List[Any]:
        """Find all entities matching a given SQLAlchemy condition."""
        with get_session() as session:
            entities = session.query(self.class_name).filter(condition).all()
            for entity in entities:
                session.expunge(entity)
            return entities
