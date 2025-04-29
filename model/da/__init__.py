"""
model/da/__init__.py
--------------------
This package provides Data Access Layer (DAL) functionalities.

It abstracts the low-level database interactions using SQLAlchemy and exposes:
- Session management
- Generic CRUD operations
- Report-oriented data queries

Modules included:
- config         : Database configuration and initialization
- session        : Session manager with context control
- base_access    : Generic DataAccess class for CRUD operations
- reports        : Report-specific advanced queries for analytics

Usage Example:
--------------
from model.da.base_access import DataAccess
from model.da.reports import get_current_borrows_with_details
"""

# Session and DB Management
from model.da.config import DB_CONFIG, initialize_database
from model.da.session import get_session

# Core Data Access
from model.da.base_access import DataAccess

# Reporting Utilities
from model.da.reports import (
    get_current_borrows_with_details,
    get_books_never_borrowed,
    get_members_with_unreturned_books,
    get_report_all_borrows,
    get_members_never_borrowed,
    get_book_borrow_counts,
)
