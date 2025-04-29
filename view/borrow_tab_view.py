"""
view/borrow_tab_view.py
------------------------
This module implements the BorrowView class, which provides a GUI for managing
borrow records. It uses custom components for text entry, autocomplete comboboxes,
date entry fields, and a table to display borrow data. It also handles user actions
such as save, edit, delete, and refresh operations on borrow records.
"""

from datetime import date
import tkinter as tk
from tkinter import Button, ttk, messagebox as msg
from typing import List, Tuple, Union
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
    A tabbed interface for managing borrow records.
    Provides form input, table display, and interaction logic.
    """

    def __init__(self, parent):
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
        """Load member and book data using controller functions."""
        members_status, members_data = find_all_members()
        self.members = members_data if members_status else []
        if not members_status:
            msg.showerror("Error", f"Failed to load members: {members_data}")

        books_status, books_data = find_all_books()
        self.books = books_data if books_status else []
        if not books_status:
            msg.showerror("Error", f"Failed to load books: {books_data}")

    def _create_member_and_book_input_fields(self) -> None:
        """Create and position input fields for Borrow ID, Member, and Book."""
        self.borrow_id = LabelAndEntry(
            self,
            25,
            "Borrow ID",
            self.entries_x,
            self.entries_y,
            self.x_distance,
            "int",
            "readonly",
        )
        self.member = LabelAndCombo(
            self,
            25,
            "Member",
            self.entries_x,
            self.entries_y + self.y_distance,
            self.x_distance,
            [f"{m.id}-{m.name} {m.family}" for m in self.members],
        )
        self.book = LabelAndCombo(
            self,
            25,
            "Book",
            self.entries_x,
            self.entries_y + 2 * self.y_distance,
            self.x_distance,
            [f"{b.id}-{b.title} by {b.author}" for b in self.books],
        )

    def _create_date_input_fields(self) -> None:
        """Create and position date input fields for Borrow Date and Return Date."""
        self.borrow_date = LabelAndDate(
            self,
            25,
            "Borrow Date",
            self.entries_x,
            self.entries_y + 3 * self.y_distance,
            self.x_distance,
        )
        self.return_date = LabelAndDate(
            self,
            25,
            "Return Date",
            self.entries_x,
            self.entries_y + 4 * self.y_distance,
            self.x_distance,
        )
        self.borrow_date.date_entry.delete(0, tk.END)
        self.return_date.date_entry.delete(0, tk.END)

    def _create_borrow_table(self) -> None:
        """Create the table to display borrow records."""
        self.borrow_table = Table(
            self,
            ["Borrow ID", "Member ID", "Book ID", "Borrow Date", "Return Date"],
            [90, 90, 90, 110, 110],
            280,
            20,
            self._load_selected_borrow,
            11,
        )

    def _load_selected_borrow(self, values: List[str]) -> None:
        """Load data from a selected row in the table into the input fields."""
        try:
            self.borrow_id.variable.set(int(values[0]))
            member = next((m for m in self.members if m._id == int(values[1])), None)
            if member:
                self.member.combo.set(f"{member.id}-{member.name} {member.family}")
                self.member.combo.hide_list()

            book = next((b for b in self.books if b._id == int(values[2])), None)
            if book:
                self.book.combo.set(f"{book.id}-{book.title} by {book.author}")
                self.book.combo.hide_list()

            (
                self.borrow_date.date_entry.set_date(values[3])
                if values[3] != "None"
                else self.borrow_date.date_entry._set_text("")
            )
            (
                self.return_date.date_entry.set_date(values[4])
                if values[4] != "None"
                else self.return_date.date_entry._set_text("")
            )

        except (ValueError, IndexError) as e:
            msg.showerror("Load Error", f"Invalid data selection: {str(e)}")

    def _refresh_table_data(self) -> None:
        """Reload the table with the latest borrow records from the database."""
        status, borrow_list = find_all_borrows()
        self.borrow_table.show_data(borrow_list)

    def _reset_form_unless_dates(self) -> None:
        """Reset non-date input fields and refresh the table."""
        self.borrow_id.variable.set(0)
        self.member.combo.set("")
        self.book.combo.set("")
        self._refresh_table_data()
        self.member.combo.focus_set()

    def _reset_dates(self) -> None:
        """Rebuild DateEntry widgets to ensure internal state is reset."""
        self.borrow_date.date_entry.destroy()
        self.return_date.date_entry.destroy()
        self._create_date_input_fields()

    def _reset_whole_form(self) -> None:
        """Completely reset all input fields and date fields."""
        self._reset_dates()
        self._reset_form_unless_dates()

    def _create_action_buttons(self) -> None:
        """Create Save, Edit, Delete, and Refresh buttons."""
        base_y = 210
        btn_x_distance = 70
        btn_y_distance = 30
        btn_width = 7

        Button(self, text="Save", command=self.save_click, width=btn_width).place(
            x=20, y=base_y
        )
        Button(self, text="Edit", command=self.edit_click, width=btn_width).place(
            x=20 + btn_x_distance, y=base_y
        )
        Button(self, text="Delete", command=self.delete_click, width=btn_width).place(
            x=20 + 2 * btn_x_distance, y=base_y
        )
        Button(self, text="Refresh", command=self._reset_whole_form, width=27).place(
            x=20, y=base_y + btn_y_distance
        )

    def save_click(self) -> None:
        """Handle saving a new borrow record."""
        borrow = self._get_borrow_from_input()
        if borrow:
            status, saved = add_borrow(*borrow)
            if status:
                self._reset_whole_form()
                msg.showinfo("Save Borrow", "Borrow saved successfully.")
            else:
                msg.showerror("Save Error", str(saved))

    def edit_click(self) -> None:
        """Handle editing an existing borrow record."""
        borrow_id = self.borrow_id.variable.get()
        if borrow_id == 0:
            msg.showerror("Error", "No borrow is selected!")
            return
        borrow = self._get_borrow_from_input()
        if borrow:
            status, edited = edit_borrow(borrow_id, *borrow)
            if status:
                self._reset_whole_form()
                msg.showinfo("Edit Borrow", "Borrow information successfully updated.")
            else:
                msg.showerror("Edit Error", str(edited))

    def delete_click(self) -> None:
        """Handle deleting the selected borrow record."""
        borrow_id = self.borrow_id.variable.get()
        if borrow_id == 0:
            msg.showerror("Error", "No borrow is selected!")
            return
        status, removed = remove_borrow_by_id(id=borrow_id)
        if status:
            self._reset_whole_form()
            msg.showinfo("Delete Borrow", "Borrow successfully deleted.")
        else:
            msg.showerror("Delete Error", str(removed))

    def _get_borrow_from_input(
        self,
    ) -> Union[Tuple[int, int, date, Union[date, None]], None]:
        """Extract input values and return a validated borrow tuple."""
        member_val = self.member.combo.get()
        if not member_val:
            msg.showerror("Validation Error", "Please select a member.")
            return
        member_id = int(member_val.split("-")[0])

        book_val = self.book.combo.get()
        if not book_val:
            msg.showerror("Validation Error", "Please select a book.")
            return
        book_id = int(book_val.split("-")[0])

        borrow_date = (
            self.borrow_date.date_entry.get_date()
            if self.borrow_date.date_entry.get()
            else date.today()
        )
        return_date = (
            self.return_date.date_entry.get_date()
            if self.return_date.date_entry.get()
            else None
        )

        if member_id <= 0:
            msg.showerror("Validation Error", "Member ID not valid!")
            return
        if book_id <= 0:
            msg.showerror("Validation Error", "Book ID not valid!")
            return

        return (member_id, book_id, borrow_date, return_date)
