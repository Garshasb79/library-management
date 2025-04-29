"""
model/entity/__init__.py
------------------------
Centralized import module for the entity (model) layer of the application.

This module provides convenient access to all SQLAlchemy ORM entity classes used 
to represent core business models within the database.

Exposed Entities:
- Base: Declarative base class shared by all ORM models.
- Member: Represents a library member (name, family).
- Book: Represents a book (title, author, pages).
- Borrow: Represents a borrowing record between a member and a book.

Typical usage:
    from model.entity import Member, Book, Borrow

This file also ensures access to common validation and logging tools needed for model logic.
"""

# # Standard Library
# from datetime import date

# SQLAlchemy Core
# from sqlalchemy import Column, String, Integer, Date, ForeignKey
# from sqlalchemy.orm import relationship

# Internal Utilities
from model.tools.validators import *
from model.tools.logger import Logger

# Entity Classes
from model.entity.base import Base
from model.entity.member import Member
from model.entity.book import Book
from model.entity.borrow import Borrow

