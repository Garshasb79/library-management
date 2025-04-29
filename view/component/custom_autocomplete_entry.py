"""
view/component/custom_autocomplete_entry.py
-------------------------------------------
Defines CustomAutocompleteEntry, an enhanced Entry widget with autocomplete support.

Features:
- Suggestion dropdown (Listbox in a Toplevel popup)
- Real-time filtering
- Keyboard and mouse navigation
- Integration-ready for custom forms
"""

import tkinter as tk
from typing import List, Optional


class CustomAutocompleteEntry(tk.Entry):
    """
    A custom Tkinter Entry widget with autocomplete suggestion popup.
    """

    def __init__(self, master: tk.Widget, completevalues: List[str], **kwargs) -> None:
        """
        Initialize the autocomplete entry.

        Args:
            master: Parent widget.
            completevalues: List of string suggestions.
            kwargs: Standard tk.Entry options.
        """
        allowed_keys = {
            "bg",
            "fg",
            "font",
            "justify",
            "relief",
            "state",
            "width",
            "xscrollcommand",
            "highlightcolor",
            "highlightthickness",
            "insertbackground",
            "insertborderwidth",
            "insertofftime",
            "insertontime",
            "insertwidth",
            "disabledforeground",
            "readonlybackground",
            "exportselection",
            "show",
            "textvariable",
            "validate",
            "validatecommand",
            "vcmd",
        }
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_keys}
        super().__init__(master, **filtered_kwargs)

        self.completevalues: List[str] = completevalues
        self.var: tk.StringVar = tk.StringVar()
        self.configure(textvariable=self.var)
        self.var.trace_add("write", self._on_var_change)

        self._user_interaction: bool = False
        self._tab_change: bool = False

        self.bind("<Button-1>", self.on_focus_in)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)
        self.bind("<Return>", self.select_item)
        self.bind("<Escape>", lambda e: self.hide_list())

        # Popup suggestion list setup
        self.popup: tk.Toplevel = tk.Toplevel(self)
        self.popup.wm_overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.popup.withdraw()

        self.listbox: tk.Listbox = tk.Listbox(
            self.popup, exportselection=False, borderwidth=0, highlightthickness=0
        )
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<ButtonRelease-1>", self.on_listbox_click)
        self.listbox.bind("<Motion>", self.on_listbox_motion)

        self.listbox_visible: bool = False
        self.lb_index: int = 0

    def on_focus_in(self, _: tk.Event) -> None:
        """Triggered on focus to optionally show suggestion list."""
        if self._tab_change:
            self._tab_change = False
            return
        self._user_interaction = True
        if not self.listbox_visible:
            self._on_var_change()

    def on_focus_out(self, _: tk.Event) -> None:
        """Hide suggestion popup when Entry loses focus."""
        self.hide_list()

    def _on_var_change(self, *_: object) -> None:
        """Recompute suggestion list as user types."""
        text = self.var.get()
        if not self._user_interaction and text:
            self._user_interaction = True
        if not self._user_interaction:
            return

        suggestions = (
            self.completevalues
            if text == ""
            else [s for s in self.completevalues if text.lower() in s.lower()]
        )
        self.show_list(suggestions)

    def show_list(self, suggestions: List[str]) -> None:
        """Render the popup suggestion list below the Entry."""
        if not suggestions:
            self.hide_list()
            return

        self.listbox.delete(0, tk.END)
        for s in suggestions:
            self.listbox.insert(tk.END, s)

        self.update_idletasks()
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        width = self.winfo_width()
        height = min(100, 20 * len(suggestions))
        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        self.popup.deiconify()
        self.popup.lift()
        self.listbox_visible = True

        self.lb_index = 0
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.lb_index)
        self.listbox.activate(self.lb_index)

    def hide_list(self) -> None:
        """Hide the suggestion popup."""
        self.after(10, lambda: self.popup.withdraw())
        self.listbox_visible = False

    def toggle_list(self, _: Optional[tk.Event] = None) -> None:
        """Manually toggle the popup list."""
        if self.listbox_visible:
            self.hide_list()
        else:
            self._on_var_change()

    def move_down(self, _: tk.Event) -> str:
        """Keyboard ↓: Highlight next item."""
        if self.listbox_visible and self.listbox.size() > 0:
            self.lb_index = (self.lb_index + 1) % self.listbox.size()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.lb_index)
            self.listbox.activate(self.lb_index)
        return "break"

    def move_up(self, _: tk.Event) -> str:
        """Keyboard ↑: Highlight previous item."""
        if self.listbox_visible and self.listbox.size() > 0:
            self.lb_index = (self.lb_index - 1) % self.listbox.size()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.lb_index)
            self.listbox.activate(self.lb_index)
        return "break"

    def select_item(self, _: tk.Event) -> str:
        """Confirm selection via Enter key."""
        if self.listbox_visible and self.listbox.size() > 0:
            self.select_index(self.lb_index)
        return "break"

    def select_index(self, index: int) -> None:
        """Set the Entry value from selected listbox index."""
        try:
            value = self.listbox.get(index)
            self.var.set(value)
            self.icursor(tk.END)
        except tk.TclError:
            pass
        self.hide_list()

    def on_listbox_click(self, event: tk.Event) -> str:
        """Mouse click on list item."""
        index = self.listbox.nearest(event.y)
        self.select_index(index)
        return "break"

    def on_listbox_motion(self, event: tk.Event) -> None:
        """Highlight suggestion under mouse pointer."""
        index = self.listbox.nearest(event.y)
        if index != self.lb_index:
            self.lb_index = index
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.activate(index)

    def tab_changed(self) -> None:
        """External method to signal Entry was focused via tab switch."""
        self._tab_change = True
        self._user_interaction = False

    def set(self, value: str) -> None:
        """Set Entry content programmatically."""
        self.var.set(value)
        self._user_interaction = False

    def set_completion_list(self, values: List[str]) -> None:
        """Update the suggestion source list."""
        self.completevalues = values
