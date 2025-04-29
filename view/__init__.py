"""
view.__init__.py
----------------
Initializes the GUI view layer of the application.

This package contains:
- Individual tab views (Members, Books, Borrows, Reports)
- Shared UI components under `view.component`

Each view class is responsible for rendering its section of the application and handling
UI-level events.
"""

# Public imports for views
from view.borrow_tab_view import BorrowView
from view.book_tab_view import BookView
from view.member_tab_view import MemberView
from view.report_tab_view import ReportView
