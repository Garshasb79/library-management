"""
view/member_tab_view.py
------------------------
This module implements the MemberView class which provides the GUI interface
for managing library members. It includes input fields, a table display,
and actions such as saving, editing, deleting, and refreshing members.
"""

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
    GUI class to manage library members.
    Provides inputs for member data and operations such as Save, Edit, Delete.
    """

    def __init__(self, parent):
        """Initialize the MemberView layout."""
        super().__init__(parent)
        self._create_input_fields()
        self._create_member_table()
        self._reset_form()
        self._create_action_buttons()

    def _create_input_fields(self) -> None:
        """Create and position input fields for member information."""
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
        """Create the table for displaying all members."""
        self.member_table = Table(
            parent=self,
            headings=["ID", "Name", "Family"],
            column_widths=[30, 230, 230],
            x=280,
            y=20,
            on_double_click=self._load_selected_member,
            table_height=11,
        )

    def _load_selected_member(self, values: Tuple[str, str, str]) -> None:
        """Load selected member data into input fields."""
        try:
            self.id.variable.set(int(values[0]))
            self.name.variable.set(values[1])
            self.family.variable.set(values[2])
        except (ValueError, IndexError) as e:
            msg.showerror("Load Error", f"Invalid data selection: {str(e)}")

    def _refresh_table_data(self) -> None:
        """Refresh the member table with the latest data from the controller."""
        status, member_list = find_all_members()
        if status:
            self.member_table.show_data(member_list)

    def _reset_form(self) -> None:
        """Clear input fields and reload table data."""
        self.id.variable.set(0)
        self.name.variable.set("")
        self.family.variable.set("")
        self._refresh_table_data()
        self.name.entry.focus_set()

    def _create_action_buttons(self) -> None:
        """Create Save, Edit, Delete, and Refresh buttons."""
        btn_y = 210
        btn_x_distance = 70
        btn_y_distance = 30
        btn_width = 7

        Button(self, text="Save", command=self.save_click, width=btn_width).place(
            x=20, y=btn_y
        )
        Button(self, text="Edit", command=self.edit_click, width=btn_width).place(
            x=20 + btn_x_distance, y=btn_y
        )
        Button(self, text="Delete", command=self.delete_click, width=btn_width).place(
            x=20 + 2 * btn_x_distance, y=btn_y
        )
        Button(self, text="Refresh", command=self._reset_form, width=27).place(
            x=20, y=btn_y + btn_y_distance
        )

    def save_click(self) -> None:
        """Handle saving a new member record."""
        member = self._get_member_from_input()
        if member is None:
            return
        add_member(*member)
        self._reset_form()
        msg.showinfo("Save Member", "Member saved successfully.")

    def edit_click(self) -> None:
        """Handle editing an existing member record."""
        member_id = self.id.variable.get()
        if member_id == 0:
            msg.showerror("Error", "No member is selected!")
            return
        member = self._get_member_from_input()
        if member:
            status, edited = edit_member(member_id, *member)
            if status:
                self._reset_form()
                msg.showinfo("Edit Member", "Member information successfully updated.")
            else:
                msg.showerror("Edit Error", str(edited))

    def delete_click(self) -> None:
        """Handle deleting a selected member."""
        member_id = self.id.variable.get()
        if member_id == 0:
            msg.showerror("Error", "No member is selected!")
            return
        status, removed = remove_member_by_id(member_id)
        if status:
            self._reset_form()
            msg.showinfo("Delete Member", "Member successfully deleted.")
        else:
            msg.showerror("Delete Error", str(removed))

    def _get_member_from_input(self) -> Optional[Tuple[str, str]]:
        """
        Validate and return member input as a tuple: (name, family).

        Returns:
            A tuple (name, family) if valid, otherwise None.
        """
        name = self.name.variable.get()
        family = self.family.variable.get()
        if not name:
            msg.showerror("Validation Error", "Name is required!")
            return None
        if not family:
            msg.showerror("Validation Error", "Family is required!")
            return None
        return (name, family)
