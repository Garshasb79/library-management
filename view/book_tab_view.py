"""
view/book_tab_view.py
------------------------
This module implements the BookView class which provides the GUI interface
for managing library books. It includes input fields for book details,
a table for displaying records, and actions such as saving, editing,
deleting, and refreshing book entries.
"""

from tkinter import Button, ttk, messagebox as msg
from controller.book_controller import (
    add_book,
    edit_book,
    remove_book_by_id,
    find_all_books,
)
from view.component import LabelAndEntry, Table
from typing import Optional, Tuple


class BookView(ttk.Frame):
    """
    BookView GUI class for managing book records.
    
    Provides:
    - Entry fields for ID, title, author, and pages
    - A table to display existing books
    - Buttons to perform CRUD operations
    """

    def __init__(self, parent: ttk.Notebook) -> None:
        """Initialize the BookView layout and UI elements."""
        super().__init__(parent)
        self._create_input_fields()
        self._create_book_table()
        self._reset_form()
        self._create_action_buttons()

    def _create_input_fields(self) -> None:
        """Create and position input fields for book data."""
        entries_x = 20
        entries_y = 20
        x_distance = 80
        y_distance = 40

        self.id = LabelAndEntry(
            parent=self,
            width=25,
            label_text="ID",
            x=entries_x,
            y=entries_y,
            distance=x_distance,
            data_type="int",
            state="readonly",
        )
        self.title = LabelAndEntry(
            parent=self,
            width=25,
            label_text="Title",
            x=entries_x,
            y=entries_y + y_distance,
            distance=x_distance,
            data_type="str",
        )
        self.author = LabelAndEntry(
            parent=self,
            width=25,
            label_text="Author",
            x=entries_x,
            y=entries_y + 2 * y_distance,
            distance=x_distance,
            data_type="str",
        )
        self.pages = LabelAndEntry(
            parent=self,
            width=25,
            label_text="Pages",
            x=entries_x,
            y=entries_y + 3 * y_distance,
            distance=x_distance,
            data_type="int",
        )

    def _create_book_table(self) -> None:
        """Create the table to display book records."""
        status, book_list = find_all_books()
        self.book_table = Table(
            parent=self,
            headings=["ID", "Title", "Author", "Pages"],
            column_widths=[30, 160, 160, 140],
            x=270,
            y=20,
            data=book_list,
            on_double_click=self._load_selected_book,
            table_height=10,
        )
        if not status:
            msg.showerror("Load Error", f"Failed to load books: {book_list}")

    def _load_selected_book(self, values: Tuple[str, str, str, str]) -> None:
        """Load selected book data into input fields."""
        try:
            self.id.variable.set(int(values[0]))
            self.title.variable.set(values[1])
            self.author.variable.set(values[2])
            self.pages.variable.set(int(values[3]))
        except (ValueError, IndexError) as e:
            msg.showerror("Load Error", f"Invalid data selection: {e}")

    def _refresh_table_data(self) -> None:
        """Fetch and display all book records in the table."""
        status, result = find_all_books()
        if status:
            self.book_table.update_data(result)
        else:
            msg.showerror("Refresh Error", f"Could not refresh data: {result}")

    def _reset_form(self) -> None:
        """Clear all input fields and refresh the table."""
        self.id.variable.set(0)
        self.title.variable.set("")
        self.author.variable.set("")
        self.pages.variable.set(0)
        self._refresh_table_data()
        self.title.entry.focus_set()

    def _create_action_buttons(self) -> None:
        """Create Save, Edit, Delete, and Refresh buttons."""
        btn_y = 220
        btn_x_distance = 80
        btn_y_distance = 30
        btn_width = 9

        Button(self, text="Save", command=self.save_click, width=btn_width).place(
            x=20, y=btn_y
        )
        Button(self, text="Edit", command=self.edit_click, width=btn_width).place(
            x=20 + btn_x_distance, y=btn_y
        )
        Button(self, text="Delete", command=self.delete_click, width=btn_width).place(
            x=20 + 2 * btn_x_distance, y=btn_y
        )
        Button(self, text="Refresh", command=self._reset_form, width=32).place(
            x=20, y=btn_y + btn_y_distance
        )

    def save_click(self) -> None:
        """Handle saving a new book record."""
        book = self._get_book_from_input()
        if not book:
            return
        status, result = add_book(*book)
        if status:
            msg.showinfo("Save Book", "Book saved successfully.")
            self._reset_form()
        else:
            msg.showerror("Save Error", f"Could not save book: {result}")

    def edit_click(self) -> None:
        """Handle editing an existing book record."""
        book_id = self.id.variable.get()
        if book_id == 0:
            msg.showerror("Edit Error", "No book is selected!")
            return

        book = self._get_book_from_input()
        if not book:
            return

        status, result = edit_book(book_id, *book)
        if status:
            msg.showinfo("Edit Book", "Book updated successfully.")
            self._reset_form()
        else:
            msg.showerror("Edit Error", f"Could not update book: {result}")

    def delete_click(self) -> None:
        """Handle deleting the selected book record."""
        book_id = self.id.variable.get()
        if book_id == 0:
            msg.showerror("Delete Error", "No book is selected!")
            return

        status, result = remove_book_by_id(book_id)
        if status:
            msg.showinfo("Delete Book", "Book deleted successfully.")
            self._reset_form()
        else:
            msg.showerror("Delete Error", f"Could not delete book: {result}")

    def _get_book_from_input(self) -> Optional[Tuple[str, str, int]]:
        """
        Extract and validate input values.

        Returns:
            A tuple of (title, author, pages) if valid, else None.
        """
        title = self.title.variable.get().strip()
        author = self.author.variable.get().strip()
        try:
            pages = int(self.pages.variable.get())
        except ValueError:
            msg.showerror("Validation Error", "Pages must be an integer!")
            return None

        if not title:
            msg.showerror("Validation Error", "Title is required!")
            return None
        if not author:
            msg.showerror("Validation Error", "Author is required!")
            return None
        if pages <= 0:
            msg.showerror("Validation Error", "Pages must be greater than 0!")
            return None

        return title, author, pages
