"""
view/component/table.py
-----------------------
Reusable GUI Table component built with Tkinter + ttk.Treeview.

Features:
- Supports column-based sorting (clickable headers)
- Filter bar with real-time search
- Scrollable and resizable container
- Double-click row event handler (optional)
"""

import tkinter as tk
from tkinter import ttk, Entry, StringVar
from typing import Any, Callable, List, Optional, Tuple


class Table:
    """
    A customizable and sortable table widget with filtering support.

    This widget uses a Treeview to display tabular data, with a filter entry box
    and sorting by column headers. Suitable for embedding in Tkinter forms.
    """

    def __init__(
        self,
        parent: tk.Widget,
        headings: List[str],
        column_widths: List[int],
        x: int,
        y: int,
        data: List[Tuple[Any, ...]],
        on_double_click: Optional[Callable[[Optional[Tuple[str, ...]]], None]] = None,
        table_height: int = 5,
    ) -> None:
        """
        Initialize the table widget.

        Args:
            parent (tk.Widget): Parent container.
            headings (List[str]): Column headers.
            column_widths (List[int]): Width for each column.
            x (int): X-coordinate placement.
            y (int): Y-coordinate placement.
            data (List[Tuple]): Initial data to populate.
            on_double_click (Callable): Optional row-click callback.
            table_height (int): Number of visible rows.
        """
        self.container = tk.Frame(parent)
        self.container.place(x=x, y=y)

        self.headings = headings
        self.column_widths = column_widths
        self.table_height = table_height
        self._original_data = data
        self._filter_active = False
        self._last_sorted_col = self.headings[0]
        self._last_reverse = False
        self.on_double_click = on_double_click

        self._build_ui()
        self._refresh_tree(self._get_filtered_data())

    def _build_ui(self) -> None:
        """Construct the table UI: filter input, Treeview, scrollbars."""
        self._placeholder_text = "Fast Filter"
        self.filter_var = StringVar()

        self.filter_entry = Entry(
            self.container, textvariable=self.filter_var, foreground="gray"
        )
        self.filter_entry.insert(0, self._placeholder_text)
        self.filter_entry.pack(fill="x")

        self.filter_entry.bind("<FocusIn>", self._on_focus_in)
        self.filter_entry.bind("<FocusOut>", self._on_focus_out)
        self.filter_var.trace_add("write", self._on_filter_change)

        table_frame = ttk.Frame(self.container)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.tree = ttk.Treeview(
            table_frame,
            columns=self.headings,
            show="headings",
            height=self.table_height,
        )

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        for idx, label in enumerate(self.headings):
            self.tree.column(
                idx, anchor="center", width=self.column_widths[idx], stretch=False
            )
            self.tree.heading(
                idx,
                text=label,
                command=lambda c=self.headings[idx]: self._on_header_click(c),
            )

        if self.on_double_click:
            self.tree.bind("<Double-1>", self._on_tree_double_click)

    def _on_tree_double_click(self, event: tk.Event) -> None:
        """Invoke callback when user double-clicks a row."""
        if self.tree.identify_region(event.x, event.y) == "cell":
            values = self._get_selected_values()
            if values and self.on_double_click:
                self.on_double_click(values)

    def _get_selected_values(self) -> Optional[Tuple[str, ...]]:
        """Return selected row values as a tuple of strings."""
        try:
            item = self.tree.selection()[0]
            return self.tree.item(item, "values")
        except IndexError:
            return None

    def _on_focus_in(self, _: tk.Event) -> None:
        """Remove placeholder text on entry focus."""
        if (
            not self._filter_active
            and self.filter_entry.get() == self._placeholder_text
        ):
            self.filter_entry.delete(0, "end")
            self.filter_entry.config(foreground="black")
            self._filter_active = True

    def _on_focus_out(self, _: tk.Event) -> None:
        """Restore placeholder text if entry is empty."""
        if not self.filter_entry.get().strip():
            self._filter_active = False
            self.filter_entry.insert(0, self._placeholder_text)
            self.filter_entry.config(foreground="gray")

    def _on_filter_change(self, *_: Any) -> None:
        """Refresh table when filter text changes."""
        if self._filter_active:
            self._refresh_tree(self._get_filtered_data())

    def _on_header_click(self, col: str) -> None:
        """Sort by clicked column, toggling ascending/descending."""
        if self._last_sorted_col == col:
            self._last_reverse = not self._last_reverse
        else:
            self._last_sorted_col = col
            self._last_reverse = False
        self._refresh_tree(self._get_filtered_data())

    def _get_filtered_data(self) -> List[Tuple[Any, ...]]:
        """
        Apply search filter and sort current data.

        Returns:
            List[Tuple]: Filtered and sorted dataset.
        """
        query = self.filter_var.get().lower().strip()
        filtered = [
            row
            for row in self._original_data
            if not self._filter_active
            or any(query in str(cell).lower() for cell in row)
        ]

        col_idx = self.headings.index(self._last_sorted_col)
        try:
            return sorted(
                filtered,
                key=lambda row: (
                    int(row[col_idx])
                    if str(row[col_idx]).isdigit()
                    else str(row[col_idx]).lower()
                ),
                reverse=self._last_reverse,
            )
        except Exception:
            return sorted(
                filtered,
                key=lambda row: str(row[col_idx]).lower(),
                reverse=self._last_reverse,
            )

    def _refresh_tree(self, data: List[Tuple[Any, ...]]) -> None:
        """Clear and reload Treeview with given data."""
        self.tree.delete(*self.tree.get_children())
        for item in data:
            self.tree.insert("", "end", values=item)

    def update_data(self, data: List[Tuple[Any, ...]]) -> None:
        """
        Replace data in the table and reset filter input.

        Args:
            data (List[Tuple]): New dataset to apply.
        """
        self._original_data = data
        self._filter_active = False
        self.filter_entry.delete(0, "end")
        self.filter_entry.insert(0, self._placeholder_text)
        self.filter_entry.config(foreground="gray")
        self._refresh_tree(self._get_filtered_data())
