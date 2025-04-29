"""
controller.__init__.py
-----------------------
Initializes the controller package.

This module aggregates all controller modules responsible for business logic and acts as
an abstraction layer between the GUI and the data access layer (DA).
"""

from controller import (
    book_controller,
    member_controller,
    borrow_controller,
    report_controller
)
