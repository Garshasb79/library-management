"""
model.__init__.py
-----------------
Marks the 'model' directory as a Python package.

Exposes:
- entity layer (Member, Book, Borrow, Base)
- data access layer (DataAccess)
- tools (Logger, validation)
"""

# You can expose key parts like:
from model.entity import Member, Book, Borrow, Base
from model.da import DataAccess
from model.tools.logger import Logger
from model.tools import validators
