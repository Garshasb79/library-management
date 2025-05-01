"""
model/da/base_access.py
-----------------------
Provides generic CRUD operations for any SQLAlchemy model entity.

Uses context-managed SQLAlchemy sessions to perform safe and transactional access.
Supports typical operations such as save, edit, delete, find by ID, and filtering.
"""

from typing import Type, TypeVar, Generic, List, Optional, Any
from sqlalchemy.orm import joinedload
from model.da.session import get_session

T = TypeVar("T")  # SQLAlchemy entity type


class DataAccess(Generic[T]):
    """
    Generic Data Access Object (DAO) for performing CRUD operations.

    This class allows data access operations (insert, update, delete, find)
    in a reusable and type-safe manner across all SQLAlchemy-based entities.

    Attributes:
        class_name (Type[T]): SQLAlchemy model class to operate on.
    """

    def __init__(self, class_name: Type[T]) -> None:
        """
        Initialize the DataAccess instance with a specific entity class.

        Args:
            class_name (Type[T]): The SQLAlchemy entity class to operate on.
        """
        self.class_name: Type[T] = class_name

    def save(self, entity: T) -> T:
        """
        Save a new entity to the database.

        Args:
            entity (T): The entity instance to persist.

        Returns:
            T: The saved entity (refreshed and detached from session).
        """
        with get_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            session.expunge(entity)
            return entity

    def edit(self, entity: T) -> T:
        """
        Update an existing entity in the database.

        Args:
            entity (T): The updated entity (must have a valid primary key).

        Returns:
            T: The merged (updated) entity.
        """
        with get_session() as session:
            session.merge(entity)
            session.commit()
            return entity

    def remove(self, entity: T) -> Optional[T]:
        """
        Delete an entity using its instance.

        Args:
            entity (T): The entity instance to delete (must have a valid ID).

        Returns:
            Optional[T]: The deleted entity if found and removed, otherwise None.
        """
        with get_session() as session:
            found: Optional[T] = session.get(self.class_name, entity.id)
            if found:
                session.delete(found)
                session.commit()
                return found
        return None

    def remove_by_id(self, entity_id: int) -> Optional[T]:
        """
        Delete an entity by its primary key.

        Args:
            entity_id (int): The ID of the entity to delete.

        Returns:
            Optional[T]: The deleted entity if found and removed, otherwise None.
        """
        with get_session() as session:
            found: Optional[T] = session.get(self.class_name, entity_id)
            if found:
                session.delete(found)
                session.commit()
                return found
        return None

    def find_all(self) -> List[T]:
        """
        Retrieve all records of the entity from the database.

        Returns:
            List[T]: A list of all entity instances.
        """
        with get_session() as session:
            entities: List[T] = session.query(self.class_name).all()
            for entity in entities:
                session.expunge(entity)
            return entities

    def find_by_id(self, id: int) -> Optional[T]:
        """
        Find a single entity by its primary key.

        Args:
            id (int): The ID of the entity.

        Returns:
            Optional[T]: The entity if found, otherwise None.
        """
        with get_session() as session:
            entity: Optional[T] = session.get(self.class_name, id)
            if entity:
                session.expunge(entity)
            return entity

    def find_all_by(self, condition: Any) -> List[T]:
        """
        Find all entities matching a given SQLAlchemy condition.

        Args:
            condition (Any): SQLAlchemy filter expression (e.g. Model.field == value).

        Returns:
            List[T]: List of matching entity instances.
        """
        with get_session() as session:
            entities: List[T] = session.query(self.class_name).filter(condition).all()
            for entity in entities:
                session.expunge(entity)
            return entities
