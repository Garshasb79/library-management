"""
view/report_tab_view.py
------------------------
This module implements the ReportView class which provides the GUI interface
for accessing various library reports. It includes buttons to generate and display
reports in a structured tabular format using the ReportWindow component.
"""

from tkinter import Button
from tkinter import ttk
from tkinter.ttk import Label
from controller import report_controller
from view.report_window import ReportWindow
from typing import List, Tuple, Dict


class ReportView(ttk.Frame):
    """
    ReportView GUI class for generating and displaying library reports.
    Provides buttons for each report and opens tabular result windows.
    """

    def __init__(self, master):
        """Initialize the ReportView layout."""
        super().__init__(master)
        self._build()

    def _build(self) -> None:
        """Create and layout all report buttons."""
        Label(self, text="Report Section", font=("Arial", 14, "bold")).pack(
            pady=(10, 20)
        )

        self.currently_borrowed_btn = Button(
            self,
            text="Books Currently Borrowed",
            font=("Segoe UI", 10),
            command=self.report_borrowed_books,
        )
        self.currently_borrowed_btn.pack(fill="x", padx=20, pady=4)

        Button(
            self,
            text="Books Never Borrowed",
            font=("Segoe UI", 10),
            command=self.report_never_borrowed_books,
        ).pack(fill="x", padx=20, pady=4)

        Button(
            self,
            text="Members With Unreturned Books",
            font=("Segoe UI", 10),
            command=self.report_members_with_unreturned,
        ).pack(fill="x", padx=20, pady=4)

        Button(
            self,
            text="Members Who Never Borrowed",
            font=("Segoe UI", 10),
            command=self.report_members_never_borrowed,
        ).pack(fill="x", padx=20, pady=4)

        Button(
            self,
            text="All Borrows Information",
            font=("Segoe UI", 10),
            command=self.report_all_borrows,
        ).pack(fill="x", padx=20, pady=4)

        Button(
            self,
            text="Borrow Times per Book",
            font=("Segoe UI", 10),
            command=self.book_borrow_counts,
        ).pack(fill="x", padx=20, pady=4)

    def report_borrowed_books(self) -> None:
        """Generate report for currently borrowed books."""
        data = report_controller.get_currently_borrowed_info()
        self._create_report_window(
            "Books Currently Borrowed",
            data,
            ("book_id", "book", "member_id", "first_name", "last_name", "borrow_date"),
            {
                "book_id": "Book ID",
                "book": "Book Title",
                "member_id": "Member ID",
                "first_name": "First Name",
                "last_name": "Last Name",
                "borrow_date": "Borrow Date",
            },
        )

    def report_never_borrowed_books(self) -> None:
        """Generate report for books that have never been borrowed."""
        data = report_controller.get_books_never_borrowed_info()
        self._create_report_window(
            "Books Never Borrowed",
            data,
            ("book_id", "title", "author"),
            {"book_id": "Book ID", "title": "Title", "author": "Author"},
        )

    def report_members_with_unreturned(self) -> None:
        """Generate report for members who have unreturned books."""
        data = report_controller.get_members_with_unreturned_info()
        self._create_report_window(
            "Members With Unreturned Books",
            data,
            ("member_id", "name", "family", "book_title", "delay_days"),
            {
                "member_id": "Member ID",
                "name": "First Name",
                "family": "Last Name",
                "book_title": "Book Title",
                "delay_days": "Days Since Borrowed",
            },
        )

    def report_members_never_borrowed(self) -> None:
        """Generate report for members who never borrowed any book."""
        data = report_controller.get_members_never_borrowed_info()
        self._create_report_window(
            "Members Who Never Borrowed",
            data,
            ("member_id", "name", "family"),
            {"member_id": "Member ID", "name": "First Name", "family": "Last Name"},
        )

    def report_all_borrows(self) -> None:
        """Generate report for all borrow records."""
        data = report_controller.get_report_all_borrows_info()
        self._create_report_window(
            "All Borrow Records",
            data,
            (
                "book_id",
                "book_title",
                "author",
                "member_id",
                "name",
                "family",
                "borrow_date",
                "return_date",
            ),
            {
                "book_id": "Book ID",
                "book_title": "Book Title",
                "author": "Author",
                "member_id": "Member ID",
                "name": "First Name",
                "family": "Last Name",
                "borrow_date": "Borrow Date",
                "return_date": "Return Date",
            },
        )

    def book_borrow_counts(self) -> None:
        """Generate report showing how many times each book has been borrowed."""
        data = report_controller.get_book_borrow_counts_info()
        self._create_report_window(
            "Borrow Times per Book",
            data,
            ("book_id", "title", "author", "borrow_times"),
            {
                "book_id": "Book ID",
                "title": "Title",
                "author": "Author",
                "borrow_times": "Times Borrowed",
            },
        )

    def _create_report_window(
        self,
        title: str,
        data: List[Tuple],
        columns: Tuple[str, ...],
        headings: Dict[str, str],
    ) -> None:
        """Helper method to create and display a report window."""
        ReportWindow(self, title, data, columns, headings)
