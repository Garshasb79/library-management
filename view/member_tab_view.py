"""
view/member_tab_view.py
------------------------
Implements the MemberView class, the GUI interface for managing
library members: viewing, adding, editing, and deleting records.

Features:
- Custom entry widgets with validation
- Interactive table with double-click support
- Status-aware user messaging
"""

import tkinter as tk
from tkinter import Button, ttk, messagebox as msg
from typing import Optional, Tuple

from controller.member_controller import (
    add_member,
    edit_member,
    remove_member_by_id,
    find_all_members,
)
from view.component import LabelAndEntry, Table


class MemberView(ttk.Frame):
    """
    GUI view for managing library members.

    Includes input fields and a table with action buttons for Save, Edit, Delete, and Refresh.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """
        Initialize the MemberView layout and internal widgets.

        Args:
            parent (tk.Widget): The container this frame is placed inside.
        """
        super().__init__(parent)
        self._create_input_fields()
        self._create_member_table()
        self._reset_form()
        self._create_action_buttons()

    def _create_input_fields(self) -> None:
        """Create input widgets for ID, Name, and Family fields."""
        entries_x, entries_y = 20, 20
        x_distance, y_distance = 80, 40

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
        self.name = LabelAndEntry(
            parent=self,
            width=25,
            label_text="Name",
            x=entries_x,
            y=entries_y + y_distance,
            distance=x_distance,
            data_type="str",
        )
        self.family = LabelAndEntry(
            parent=self,
            width=25,
            label_text="Family",
            x=entries_x,
            y=entries_y + 2 * y_distance,
            distance=x_distance,
            data_type="str",
        )

    def _create_member_table(self) -> None:
        """Create the table to display all current members."""
        status, result = find_all_members()
        member_list = result if status else []

        self.member_table = Table(
            parent=self,
            headings=["ID", "Name", "Family"],
            column_widths=[30, 230, 230],
            x=270,
            y=20,
            data=member_list,
            on_double_click=self._load_selected_member,
            table_height=10,
        )

        if not status:
            msg.showerror("Load Error", f"Could not load members: {result}")

    def _load_selected_member(self, values: Tuple[str, str, str]) -> None:
        """
        Populate input fields from selected row.

        Args:
            values (Tuple[str, str, str]): (ID, Name, Family)
        """
        try:
            self.id.variable.set(int(values[0]))
            self.name.variable.set(values[1])
            self.family.variable.set(values[2])
        except (ValueError, IndexError) as e:
            msg.showerror("Load Error", f"Invalid data selection: {e}")

    def _refresh_table_data(self) -> None:
        """Reload the table with updated data."""
        status, result = find_all_members()
        if status:
            self.member_table.update_data(result)
        else:
            msg.showerror("Refresh Error", f"Could not refresh data: {result}")

    def _reset_form(self) -> None:
        """Clear form and refresh member list."""
        self.id.variable.set(0)
        self.name.variable.set("")
        self.family.variable.set("")
        self._refresh_table_data()
        self.name.entry.focus_set()

    def _create_action_buttons(self) -> None:
        """Add action buttons: Save, Edit, Delete, Refresh."""
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
        """Save a new member record."""
        member = self._get_member_from_input()
        if not member:
            return

        status, result = add_member(*member)
        if status:
            msg.showinfo("Success", "Member saved successfully.")
            self._reset_form()
        else:
            msg.showerror("Save Error", f"Could not save member: {result}")

    def edit_click(self) -> None:
        """Update an existing member."""
        member_id = self.id.variable.get()
        if member_id == 0:
            msg.showerror("Error", "No member is selected!")
            return

        member = self._get_member_from_input()
        if not member:
            return

        status, result = edit_member(member_id, *member)
        if status:
            msg.showinfo("Success", "Member updated successfully.")
            self._reset_form()
        else:
            msg.showerror("Edit Error", f"Could not edit member: {result}")

    def delete_click(self) -> None:
        """Delete the selected member."""
        member_id = self.id.variable.get()
        if member_id == 0:
            msg.showerror("Error", "No member is selected!")
            return

        status, result = remove_member_by_id(member_id)
        if status:
            msg.showinfo("Success", "Member deleted successfully.")
            self._reset_form()
        else:
            msg.showerror("Delete Error", f"Could not delete member: {result}")

    def _get_member_from_input(self) -> Optional[Tuple[str, str]]:
        """
        Validate and extract name and family from input.

        Returns:
            Optional[Tuple[str, str]]: (name, family) or None if invalid.
        """
        name = self.name.variable.get().strip()
        family = self.family.variable.get().strip()

        if not name:
            msg.showerror("Validation Error", "Name is required!")
            return None
        if not family:
            msg.showerror("Validation Error", "Family is required!")
            return None

        return name, family
