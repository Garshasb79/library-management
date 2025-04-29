"""
view/main_window_launcher.py
-----------------------------
This module launches the main application window and initializes
the different tab views (Members, Books, Borrows, Reports).
It uses the tkinter GUI library with ttk.Notebook to provide a tabbed interface.
"""

from tkinter import Tk, ttk
from view import BorrowView, MemberView, BookView, ReportView


class MainApplication:
    """
    MainApplication initializes the main window and its components.

    Responsibilities:
    - Create a centralized tabbed interface for each functional area of the system
    - Load pages for Members, Books, Borrows, and Reports
    - Manage widget focus transitions between tabs
    """

    def __init__(self) -> None:
        """Constructor to set up the main window and UI tabs."""
        self.win = Tk()

        self._configure_window()
        self._create_tabs()
        self._create_pages()

        # Bind tab change event to manage focus behavior
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        self.win.mainloop()

    def _configure_window(self) -> None:
        """Configure the main window's title, size, and center it on the screen."""
        self.win.title("Books Info")
        self.win.resizable(False, False)
        self._center_win(width=800, height=320)

    def _center_win(self, width: int, height: int) -> None:
        """Center the window on the user's screen."""
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = (screen_width - width) // 3
        y = (screen_height - height) // 2
        self.win.geometry(f"{width}x{height}+{x}+{y}")

    def _create_tabs(self) -> None:
        """Initialize the tab notebook widget for holding different views."""
        self.notebook = ttk.Notebook(self.win)
        self.notebook.pack(fill="both", expand=True)

    def _create_pages(self) -> None:
        """Instantiate and add each view (tab) to the notebook."""
        self.member_page = MemberView(self.notebook)
        self.notebook.add(self.member_page, text="Members")

        self.book_page = BookView(self.notebook)
        self.notebook.add(self.book_page, text="Books")

        self.borrow_page = BorrowView(self.notebook)
        self.notebook.add(self.borrow_page, text="Borrows")

        self.report_page = ReportView(self.notebook)
        self.notebook.add(self.report_page, text="Reports")

    def _on_tab_changed(self, event) -> None:
        """
        Handle focus logic when the user switches between tabs.
        Sets initial focus to the most relevant input field in the active tab.
        """
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")

        if tab_text == "Members":
            self.win.after(100, self.member_page.name.entry.focus_set)
        elif tab_text == "Books":
            self.win.after(100, self.book_page.title.entry.focus_set)
        elif tab_text == "Borrows":
            self.win.after(100, self.borrow_page.member.combo.focus_set)
            self.borrow_page.member.combo.tab_changed()
        elif tab_text == "Reports":
            self.win.after(100, self.report_page.currently_borrowed_btn.focus_set)


if __name__ == "__main__":
    MainApplication()
