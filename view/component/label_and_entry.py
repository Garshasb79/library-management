"""
view/component/label_and_entry.py
---------------------------------
This module defines reusable GUI components used across different views.

Classes:
- LabelAndEntry: A labeled Entry widget with support for int/str types.
- LabelAndCombo: A labeled Entry with autocomplete functionality.
- LabelAndDate: A labeled DateEntry widget using tkcalendar.
"""

import tkinter as tk
from tkinter import ttk, StringVar, IntVar
from tkcalendar import DateEntry
from typing import Union, List, Optional

from view.component.custom_autocomplete_entry import CustomAutocompleteEntry


class LabelAndEntry:
    """
    A composite widget combining a Label and an Entry field.

    Supports variable binding for str/int types and optional readonly mode.
    """

    def __init__(
        self,
        parent: tk.Widget,
        width: int,
        label_text: str,
        x: int,
        y: int,
        distance: int = 70,
        data_type: str = "str",
        state: Optional[str] = None,
    ) -> None:
        """
        Initialize the LabelAndEntry widget.

        Args:
            parent: Parent Tkinter widget.
            width: Width of the Entry field.
            label_text: Label caption.
            x: X-coordinate of label.
            y: Y-coordinate of label.
            distance: Distance between label and entry.
            data_type: "str" or "int" for input type binding.
            state: Optional state for Entry widget (e.g., "readonly").
        """
        ttk.Label(parent, text=label_text, state=state).place(x=x, y=y)

        var_type = StringVar if data_type == "str" else IntVar
        self.variable: Union[StringVar, IntVar] = var_type()

        self.entry = ttk.Entry(
            parent, width=width, textvariable=self.variable, state=state
        )
        self.entry.place(x=x + distance, y=y)


class LabelAndCombo:
    """
    A composite widget combining a Label and a custom autocomplete Entry field.
    """

    def __init__(
        self,
        parent: tk.Widget,
        width: int,
        label_text: str,
        x: int,
        y: int,
        distance: int,
        values: List[str],
    ) -> None:
        """
        Initialize the LabelAndCombo widget.

        Args:
            parent: Parent widget.
            width: Width of the entry.
            label_text: Label caption.
            x: X-coordinate of label.
            y: Y-coordinate of label.
            distance: Distance between label and entry.
            values: Autocomplete suggestion list.
        """
        ttk.Label(parent, text=label_text).place(x=x, y=y)

        self.combo = CustomAutocompleteEntry(
            master=parent, completevalues=values, width=width
        )
        self.combo.place(x=x + distance, y=y)


class LabelAndDate(ttk.Frame):
    """
    A composite widget combining a Label and a DateEntry (calendar picker).
    """

    def __init__(
        self,
        parent: tk.Widget,
        width: int,
        label_text: str,
        x: int,
        y: int,
        distance: int,
    ) -> None:
        """
        Initialize the LabelAndDate widget.

        Args:
            parent: Parent widget.
            width: Width of the DateEntry field.
            label_text: Text of the label.
            x: X-coordinate of label.
            y: Y-coordinate of label.
            distance: Distance between label and date entry.
        """
        super().__init__(parent)

        ttk.Label(parent, text=label_text).place(x=x, y=y)

        self.variable: StringVar = StringVar()

        self.date_entry = DateEntry(
            parent,
            textvariable=self.variable,
            date_pattern="yyyy-mm-dd",
            width=width,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.date_entry.place(x=x + distance, y=y)
