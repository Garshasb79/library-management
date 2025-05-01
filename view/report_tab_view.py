"""
view/report_tab_view.py
------------------------
Implements the ReportView class for the GUI section that displays
various analytical and operational reports in the library system.

Reports are presented in separate pop-up windows using a table view.
Each button generates a specific report by calling the report controller.
"""

from tkinter import Button, Toplevel
from tkinter import ttk
from tkinter.ttk import Label
from controller import report_controller
from view.component import Table
from typing import List, Tuple


class ReportView(ttk.Frame):
    """
    ReportView GUI class for generating and displaying library reports.

    This class creates a vertical list of buttons, each mapped to a specific
    reporting query. Reports are shown in pop-up windows as scrollable tables.
    """

    def __init__(self, master) -> None:
        """
        Initialize the ReportView layout and attach report buttons.

        Args:
            master: The parent widget/container (typically a notebook tab).
        """
        super().__init__(master)
        self._build()

    def _build(self) -> None:
        """Create and layout all report-related buttons."""
        Label(self, text="Report Section", font=("Arial", 14, "bold")).pack(
            pady=(10, 20)
        )

        self.all_borrows_information = Button(
            self,
            text="All Borrows Information",
            font=("Segoe UI", 10),
            command=self.report_all_borrows,
        )
        self.all_borrows_information.pack(fill="x", padx=20, pady=4)

        Button(
            self,
            text="Books Currently Borrowed",
            font=("Segoe UI", 10),
            command=self.report_borrowed_books,
        ).pack(fill="x", padx=20, pady=4)

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
            text="Borrow Times per Book",
            font=("Segoe UI", 10),
            command=self.book_borrow_counts,
        ).pack(fill="x", padx=20, pady=4)

    def report_all_borrows(self) -> None:
        """Generate report: all historical borrow transactions."""
        data = report_controller.get_report_all_borrows_info()
        self._create_report_window(
            title="All Borrow Records",
            data=data,
            column_widths=[70, 150, 150, 70, 150, 150, 150, 150],
            headings=[
                "Book ID",
                "Book Title",
                "Author",
                "Member ID",
                "First Name",
                "Last Name",
                "Borrow Date",
                "Return Date",
            ],
        )

    def report_borrowed_books(self) -> None:
        """Generate report: books currently borrowed."""
        data = report_controller.get_currently_borrowed_info()
        self._create_report_window(
            title="Books Currently Borrowed",
            data=data,
            column_widths=[70, 150, 70, 150, 150, 150],
            headings=[
                "Book ID",
                "Book Title",
                "Member ID",
                "First Name",
                "Last Name",
                "Borrow Date",
            ],
        )

    def report_never_borrowed_books(self) -> None:
        """Generate report: books that have never been borrowed."""
        data = report_controller.get_books_never_borrowed_info()
        self._create_report_window(
            title="Books Never Borrowed",
            data=data,
            column_widths=[70, 150, 150],
            headings=["Book ID", "Title", "Author"],
        )

    def report_members_with_unreturned(self) -> None:
        """Generate report: members with books not returned yet."""
        data = report_controller.get_members_with_unreturned_info()
        self._create_report_window(
            title="Members With Unreturned Books",
            data=data,
            column_widths=[70, 150, 150, 150, 150],
            headings=[
                "Member ID",
                "First Name",
                "Last Name",
                "Book Title",
                "Days Since Borrowed",
            ],
        )

    def report_members_never_borrowed(self) -> None:
        """Generate report: members who have never borrowed a book."""
        data = report_controller.get_members_never_borrowed_info()
        self._create_report_window(
            title="Members Who Never Borrowed",
            data=data,
            column_widths=[70, 150, 150],
            headings=["Member ID", "First Name", "Last Name"],
        )

    def book_borrow_counts(self) -> None:
        """Generate report: how many times each book has been borrowed."""
        data = report_controller.get_book_borrow_counts_info()
        self._create_report_window(
            title="Borrow Times per Book",
            data=data,
            column_widths=[70, 150, 150, 150],
            headings=[
                "Book ID",
                "Title",
                "Author",
                "Times Borrowed",
            ],
        )

    def _create_report_window(
        self,
        title: str,
        data: List[Tuple],
        column_widths: List[int],
        headings: List[str],
    ) -> None:
        """
        Helper method to display a new window with a Table of report data.

        Args:
            title (str): Title of the window.
            data (List[Tuple]): Report data in tuple format.
            column_widths (List[int]): Column widths in pixels.
            headings (List[str]): Column headers.
        """
        window = Toplevel()
        window.title(title)

        table = Table(
            parent=window,
            headings=headings,
            column_widths=column_widths,
            x=10,
            y=10,
            data=data,
            on_double_click=None,
            table_height=20,
        )
        table.container.pack(padx=10, pady=10, fill="both", expand=True)

        # Resize window based on content size
        window.update_idletasks()
        window.geometry(
            f"{table.container.winfo_reqwidth()}x{table.container.winfo_reqheight()}"
        )
