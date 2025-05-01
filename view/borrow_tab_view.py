"""
view/borrow_tab_view.py
------------------------
This module implements the BorrowView class, which provides a GUI for managing
borrow records. It uses custom components for text entry, autocomplete comboboxes,
date entry fields, and a table to display borrow data. It also handles user actions
such as save, edit, delete, and refresh operations on borrow records.
"""

import tkinter as tk
from tkinter import Button, ttk, messagebox as msg
from datetime import date
from typing import List, Tuple, Union, Optional

from controller.borrow_controller import (
    add_borrow,
    edit_borrow,
    remove_borrow_by_id,
    find_all_borrows,
)
from controller.book_controller import find_all_books
from controller.member_controller import find_all_members
from view.component import LabelAndEntry, LabelAndCombo, LabelAndDate, Table


class BorrowView(ttk.Frame):
    """
    A tabbed interface (view) for managing borrow records in the system.

    This class allows the user to:
    - Add/edit/delete borrow records
    - View existing borrows in a table
    - Select members/books with autocomplete
    - Choose borrow and return dates
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the BorrowView layout and components."""
        super().__init__(parent)
        self.entries_x = 20
        self.entries_y = 20
        self.x_distance = 80
        self.y_distance = 40

        self._load_members_and_books()
        self._create_member_and_book_input_fields()
        self._create_date_input_fields()
        self._create_borrow_table()
        self._reset_form_unless_dates()
        self._create_action_buttons()

    def _load_members_and_books(self) -> None:
        """Load member and book data from controller to populate comboboxes."""
        members_status, members_data = find_all_members()
        self.members = members_data if members_status else []
        if not members_status:
            msg.showerror("Load Error", f"Failed to load members: {members_data}")

        books_status, books_data = find_all_books()
        self.books = books_data if books_status else []
        if not books_status:
            msg.showerror("Load Error", f"Failed to load books: {books_data}")

    def _create_member_and_book_input_fields(self) -> None:
        """Create and layout the ID, Member, and Book selection widgets."""
        self.borrow_id = LabelAndEntry(
            self, 25, "Borrow ID", self.entries_x, self.entries_y, self.x_distance, "int", "readonly"
        )
        self.member = LabelAndCombo(
            self,
            25,
            "Member",
            self.entries_x,
            self.entries_y + self.y_distance,
            self.x_distance,
            [f"{m[0]}-{m[1]} {m[2]}" for m in self.members],
        )
        self.book = LabelAndCombo(
            self,
            25,
            "Book",
            self.entries_x,
            self.entries_y + 2 * self.y_distance,
            self.x_distance,
            [f"{b[0]}-{b[1]} by {b[2]}" for b in self.books],
        )

    def _create_date_input_fields(self) -> None:
        """Create widgets to enter borrow and return dates."""
        self.borrow_date = LabelAndDate(
            self, 22, "Borrow Date", self.entries_x, self.entries_y + 3 * self.y_distance, self.x_distance
        )
        self.return_date = LabelAndDate(
            self, 22, "Return Date", self.entries_x, self.entries_y + 4 * self.y_distance, self.x_distance
        )
        self.borrow_date.date_entry.delete(0, tk.END)
        self.return_date.date_entry.delete(0, tk.END)

    def _create_borrow_table(self) -> None:
        """Create the table to display all borrow records."""
        status, borrow_list = find_all_borrows()
        self.borrow_table = Table(
            parent=self,
            headings=["Borrow ID", "Member ID", "Book ID", "Borrow Date", "Return Date"],
            column_widths=[90, 90, 90, 110, 110],
            x=270,
            y=20,
            data=borrow_list,
            on_double_click=self._load_selected_borrow,
            table_height=10,
        )

    def _load_selected_borrow(self, values: List[str]) -> None:
        """Populate form fields with the selected borrow record's data."""
        try:
            self.borrow_id.variable.set(int(values[0]))

            member = next((m for m in self.members if m[0] == int(values[1])), None)
            if member:
                self.member.combo.set(f"{member[0]}-{member[1]} {member[2]}")
                self.member.combo.hide_list()

            book = next((b for b in self.books if b[0] == int(values[2])), None)
            if book:
                self.book.combo.set(f"{book[0]}-{book[1]} by {book[2]}")
                self.book.combo.hide_list()

            self.borrow_date.date_entry.set_date(values[3]) if values[3] != "None" else self.borrow_date.date_entry._set_text("")
            self.return_date.date_entry.set_date(values[4]) if values[4] != "None" else self.return_date.date_entry._set_text("")
        except (ValueError, IndexError) as e:
            msg.showerror("Load Error", f"Invalid data selection: {e}")

    def _refresh_table_data(self) -> None:
        """Reload the borrow table with updated data from the controller."""
        status, result = find_all_borrows()
        if status:
            self.borrow_table.update_data(result)
        else:
            msg.showerror("Refresh Error", f"Could not refresh borrow data: {result}")

    def _reset_form_unless_dates(self) -> None:
        """Reset member/book/ID fields and table, keeping date inputs unchanged."""
        self.borrow_id.variable.set(0)
        self.member.combo.set("")
        self.member.combo.hide_list()
        self.book.combo.set("")
        self.book.combo.hide_list()
        self._refresh_table_data()
        self.member.combo.focus_set()

    def _reset_dates(self) -> None:
        """Destroy and recreate date widgets to reset them."""
        self.borrow_date.date_entry.destroy()
        self.return_date.date_entry.destroy()
        self._create_date_input_fields()

    def _reset_whole_form(self) -> None:
        """Reset the entire form: ID, combos, dates, and table."""
        self._reset_dates()
        self._reset_form_unless_dates()

    def _create_action_buttons(self) -> None:
        """Create action buttons and position them below the form."""
        base_y = 220
        btn_x_distance = 80
        btn_y_distance = 30
        btn_width = 9

        Button(self, text="Save", command=self.save_click, width=btn_width).place(x=20, y=base_y)
        Button(self, text="Edit", command=self.edit_click, width=btn_width).place(x=20 + btn_x_distance, y=base_y)
        Button(self, text="Delete", command=self.delete_click, width=btn_width).place(x=20 + 2 * btn_x_distance, y=base_y)
        Button(self, text="Refresh", command=self._reset_whole_form, width=32).place(x=20, y=base_y + btn_y_distance)

    def save_click(self) -> None:
        """Handle the save action for a new borrow entry."""
        borrow = self._get_borrow_from_input()
        if not borrow:
            return
        status, result = add_borrow(*borrow)
        if status:
            self._reset_whole_form()
            msg.showinfo("Save Borrow", "Borrow saved successfully.")
        else:
            msg.showerror("Save Error", f"Could not save borrow: {result}")

    def edit_click(self) -> None:
        """Handle updating an existing borrow record."""
        borrow_id = self.borrow_id.variable.get()
        if borrow_id == 0:
            msg.showerror("Error", "No borrow is selected!")
            return

        borrow = self._get_borrow_from_input()
        if not borrow:
            return

        status, result = edit_borrow(borrow_id, *borrow)
        if status:
            self._reset_whole_form()
            msg.showinfo("Edit Borrow", "Borrow updated successfully.")
        else:
            msg.showerror("Edit Error", f"Could not update borrow: {result}")

    def delete_click(self) -> None:
        """Handle deletion of a selected borrow entry."""
        borrow_id = self.borrow_id.variable.get()
        if borrow_id == 0:
            msg.showerror("Error", "No borrow is selected!")
            return

        status, result = remove_borrow_by_id(borrow_id)
        if status:
            self._reset_whole_form()
            msg.showinfo("Delete Borrow", "Borrow deleted successfully.")
        else:
            msg.showerror("Delete Error", f"Could not delete borrow: {result}")

    def _get_borrow_from_input(self) -> Optional[Tuple[int, int, date, Optional[date]]]:
        """
        Validate and extract borrow form data.

        Returns:
            A tuple (member_id, book_id, borrow_date, return_date) if valid; otherwise None.
        """
        member_val = self.member.combo.get()
        if not member_val:
            msg.showerror("Validation Error", "Please select a member.")
            return None
        member_id = int(member_val.split("-")[0])

        book_val = self.book.combo.get()
        if not book_val:
            msg.showerror("Validation Error", "Please select a book.")
            return None
        book_id = int(book_val.split("-")[0])

        borrow_date = self.borrow_date.date_entry.get_date() if self.borrow_date.date_entry.get() else date.today()
        return_date = self.return_date.date_entry.get_date() if self.return_date.date_entry.get() else None

        return member_id, book_id, borrow_date, return_date
