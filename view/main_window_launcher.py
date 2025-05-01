"""
view/main_window_launcher.py
-----------------------------
Launches the main application window and initializes
the tab-based GUI using Tkinter's ttk.Notebook.

Tabs:
- Members
- Books
- Borrows
- Reports
"""

from tkinter import Tk, ttk
from view import BorrowView, MemberView, BookView, ReportView


class MainApplication:
    """
    Main GUI application class that creates the root window and manages tab views.

    Responsibilities:
    - Initializes the main window
    - Loads tabs: Members, Books, Borrows, Reports
    - Manages focus behavior when switching tabs
    """

    def __init__(self) -> None:
        """
        Initialize the main application window and start the mainloop.
        """
        self.win = Tk()
        self._configure_window()
        self._create_tabs()
        self._create_pages()
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)
        self.win.mainloop()

    def _configure_window(self) -> None:
        """
        Set window title, size, disable resizing, and center on screen.
        """
        self.win.title("Library Management System")
        self.win.resizable(False, False)
        self._center_win(width=800, height=320)

    def _center_win(self, width: int, height: int) -> None:
        """
        Center the application window on the screen.

        Args:
            width (int): Desired window width.
            height (int): Desired window height.
        """
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        x = (screen_width - width) // 3
        y = (screen_height - height) // 2
        self.win.geometry(f"{width}x{height}+{x}+{y}")

    def _create_tabs(self) -> None:
        """
        Create the Notebook widget that holds all tab views.
        """
        self.notebook = ttk.Notebook(self.win)
        self.notebook.pack(fill="both", expand=True)

    def _create_pages(self) -> None:
        """
        Instantiate each tab view and add to the notebook.
        """
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
        Automatically focus the primary field/widget of each tab when switched.

        Args:
            event: The event object from <<NotebookTabChanged>>.
        """
        current_tab = self.notebook.select()
        tab_text = self.notebook.tab(current_tab, "text")

        # Set logical focus based on selected tab
        if tab_text == "Members":
            self.win.after(100, self.member_page.name.entry.focus_set)
        elif tab_text == "Books":
            self.win.after(100, self.book_page.title.entry.focus_set)
        elif tab_text == "Borrows":
            self.win.after(100, self.borrow_page.member.combo.focus_set)
        elif tab_text == "Reports":
            self.win.after(100, self.report_page.all_borrows_information.focus_set)


if __name__ == "__main__":
    MainApplication()
