from tkinter import Toplevel, Entry, StringVar
from tkinter import ttk
from typing import List, Tuple, Dict, Any


class ReportWindow:
    """
    ReportWindow
    ------------
    A popup window to display tabular report data with sortable columns,
    vertical scroll, and fast keyword filtering.

    Features:
    - Treeview widget with headings.
    - Clickable column headers for sorting.
    - Fast filter with placeholder.
    - Preserves current sort state while filtering.
    - Automatically sorts initially by the first column (ascending).
    """

    def __init__(
        self,
        parent,
        title: str,
        data: List[Tuple[Any, ...]],
        columns: List[str],
        headings: Dict[str, str],
    ) -> None:
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.title(title)

        self.columns: List[str] = columns
        self.headings: Dict[str, str] = headings
        self._original_data: List[Tuple[Any, ...]] = data
        self._filter_active: bool = False
        self._last_sorted_col: str = columns[0]
        self._last_reverse: bool = False

        self._build_ui()
        self._refresh_tree(self._get_filtered_data())

    def _build_ui(self) -> None:
        """Create and layout the filter entry and Treeview table with scrollbar."""
        self._placeholder_text = "Fast Filter"
        self.filter_var = StringVar()

        self.filter_entry = Entry(
            self.window, textvariable=self.filter_var, foreground="gray"
        )
        self.filter_entry.insert(0, self._placeholder_text)
        self.filter_entry.pack(padx=10, pady=5, fill="x")

        self.filter_entry.bind("<FocusIn>", self._on_focus_in)
        self.filter_entry.bind("<FocusOut>", self._on_focus_out)
        self.filter_var.trace_add("write", self._on_filter_change)

        frame = ttk.Frame(self.window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(frame, columns=self.columns, show="headings")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        for col in self.columns:
            self.tree.heading(
                col,
                text=self.headings[col],
                command=lambda c=col: self._on_column_click(c),
            )
            self.tree.column(col, anchor="center", width=120)

    def _on_focus_in(self, _) -> None:
        """Handle focus-in event: remove placeholder and activate filter."""
        if (
            not self._filter_active
            and self.filter_entry.get() == self._placeholder_text
        ):
            self.filter_entry.delete(0, "end")
            self.filter_entry.config(foreground="black")
            self._filter_active = True

    def _on_focus_out(self, _) -> None:
        """Handle focus-out event: restore placeholder if entry is empty."""
        if not self.filter_entry.get().strip():
            self._filter_active = False
            self.filter_entry.insert(0, self._placeholder_text)
            self.filter_entry.config(foreground="gray")

    def _on_filter_change(self, *_: Any) -> None:
        """Triggered when the filter text changes."""
        if self._filter_active:
            self._refresh_tree(self._get_filtered_data())

    def _on_column_click(self, col: str) -> None:
        """Handle column header click: toggle sort direction and refresh tree."""
        if self._last_sorted_col == col:
            self._last_reverse = not self._last_reverse
        else:
            self._last_sorted_col = col
            self._last_reverse = False  # reset to ascending

        self._refresh_tree(self._get_filtered_data())

    def _get_filtered_data(self) -> List[Tuple[Any, ...]]:
        """Return filtered and sorted data based on current state."""
        query = self.filter_var.get().lower().strip()
        filtered = [
            row
            for row in self._original_data
            if not self._filter_active
            or any(query in str(cell).lower() for cell in row)
        ]
        col_idx = self.columns.index(self._last_sorted_col)
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
        """Clear and repopulate Treeview with given data."""
        self.tree.delete(*self.tree.get_children())
        for item in data:
            self.tree.insert("", "end", values=item)
