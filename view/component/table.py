from tkinter import ttk
import tkinter as tk
from typing import Callable, List, Optional, Union, Tuple


class Table:
    """
    A reusable Treeview-based table widget with optional double-click and sorting behavior.
    Automatically adds a vertical scrollbar aligned with the Treeview height.
    """

    def __init__(
        self,
        parent,
        headings: List[str],
        column_widths: List[int],
        x: int,
        y: int,
        on_double_click: Optional[Callable[[Optional[Tuple[str, ...]]], None]] = None,
        table_height: int = 5,
    ) -> None:
        """
        Initialize the Table widget.

        Args:
            parent: Parent Tkinter widget.
            headings: Column names as strings.
            column_widths: Width of each column in pixels.
            x: X coordinate for placement.
            y: Y coordinate for placement.
            on_double_click: Optional function triggered on row double-click.
            table_height: Number of rows to show.
        """
        self.container = tk.Frame(parent)
        self.container.place(x=x, y=y)

        self.tree = ttk.Treeview(
            self.container,
            columns=headings,
            show="headings",
            selectmode="browse",
            height=table_height,
        )

        for idx, heading in enumerate(headings):
            self.tree.heading(
                idx, text=heading, command=lambda c=idx: self._sort_treeview(c)
            )
            self.tree.column(
                idx, width=column_widths[idx], anchor="center", stretch=False
            )

        self.vsb = ttk.Scrollbar(self.container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.vsb.grid(row=0, column=1, sticky="ns")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        if on_double_click:
            self.tree.bind(
                "<Double-1>", lambda e: self._handle_double_click(e, on_double_click)
            )

        self._sort_state = {}

    def _handle_double_click(
        self, event, callback: Callable[[Optional[Tuple[str, ...]]], None]
    ) -> None:
        """
        Trigger callback only if a row (not heading) is double-clicked.
        """
        region = self.tree.identify_region(event.x, event.y)
        if region == "cell":
            values = self.get_selected_values()
            if values is not None:
                callback(values)

    def show_data(self, data: List[Union[Tuple, object]]) -> None:
        """
        Populate the table with a list of records.

        Args:
            data: A list of tuples or objects with a `to_tuple()` method.
        """
        self.tree.delete(*self.tree.get_children())
        for item in data:
            values = item.to_tuple() if hasattr(item, "to_tuple") else item
            self.tree.insert("", "end", values=values)

        # After inserting data, sort by ID (first column) ascending
        if self.tree.get_children():
            self._sort_treeview(0)

    def get_selected_values(self) -> Optional[Tuple[str, ...]]:
        """
        Return the selected row values as a tuple, or None if nothing selected.

        Returns:
            A tuple of selected values, or None.
        """
        try:
            item = self.tree.selection()[0]
            return self.tree.item(item, "values")
        except IndexError:
            return None

    def _sort_treeview(self, col: int) -> None:
        """
        Sort the table by a specific column index.

        Args:
            col: Index of the column to sort by.
        """
        reverse = self._sort_state.get(col, False)
        items = []

        for row_id in self.tree.get_children(""):
            cell_value = self.tree.set(row_id, col)
            items.append((cell_value, row_id))

        try:
            items.sort(
                key=lambda t: int(t[0]) if str(t[0]).isdigit() else str(t[0]).lower(),
                reverse=reverse,
            )
        except Exception:
            items.sort(key=lambda t: str(t[0]).lower(), reverse=reverse)

        for index, (_, row_id) in enumerate(items):
            self.tree.move(row_id, "", index)

        self._sort_state[col] = not reverse
        self.tree.heading(col, command=lambda: self._sort_treeview(col))
