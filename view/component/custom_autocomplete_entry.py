"""
view/component/custom_autocomplete_entry.py
-------------------------------------------
Defines CustomAutocompleteEntry, an enhanced Entry widget with autocomplete support.

Features:
- Suggestion dropdown (Listbox in a Toplevel popup)
- Real-time filtering on typing
- Keyboard and mouse navigation
- Integration-ready for custom forms
"""

import tkinter as tk
from typing import List, Optional


class CustomAutocompleteEntry(tk.Entry):
    """
    A custom Tkinter Entry widget with autocomplete functionality.

    This widget shows a dropdown list of suggestions based on real-time user input.
    Suggestions are provided via a list of strings. Popup appears on typing or click,
    and disappears on focus out or selection.
    """

    def __init__(self, master: tk.Widget, completevalues: List[str], **kwargs) -> None:
        """
        Initialize the autocomplete entry widget.

        Args:
            master (tk.Widget): Parent container.
            completevalues (List[str]): List of suggestion strings.
            **kwargs: Valid arguments for tk.Entry widget.
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

        self._user_typing: bool = False  # Only show popup if triggered by user

        # Key/mouse bindings
        self.bind("<Button-1>", self._on_mouse_click)
        self.bind("<Key>", self._on_key_press)
        self.bind("<FocusOut>", self._on_focus_out)
        self.bind("<Down>", self.move_down)
        self.bind("<Up>", self.move_up)
        self.bind("<Return>", self.select_item)
        self.bind("<Escape>", lambda e: self.hide_list())

        # Suggestion popup (Toplevel) and listbox inside it
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

    def _on_mouse_click(self, event: tk.Event) -> None:
        """Trigger popup on mouse click."""
        self._user_typing = True
        self._on_var_change()

    def _on_key_press(self, event: tk.Event) -> None:
        """Track keypress to trigger suggestions."""
        self._user_typing = True

    def _on_var_change(self, *_: object) -> None:
        """Recalculate suggestions and update listbox."""
        if not self._user_typing:
            return

        text = self.var.get()
        suggestions = (
            self.completevalues
            if text == ""
            else [s for s in self.completevalues if text.lower() in s.lower()]
        )
        self.show_list(suggestions)

    def _on_focus_out(self, _: tk.Event) -> None:
        """Hide suggestion popup when focus is lost."""
        self.hide_list()

    def show_list(self, suggestions: List[str]) -> None:
        """
        Show suggestion list in a popup below the Entry.

        Args:
            suggestions (List[str]): Items to display in the popup.
        """
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
        height = min(100, 20 * len(suggestions))  # Cap popup height
        self.popup.geometry(f"{width}x{height}+{x}+{y}")
        self.popup.deiconify()
        self.popup.lift()
        self.listbox_visible = True

        self.lb_index = 0
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.lb_index)
        self.listbox.activate(self.lb_index)

    def hide_list(self) -> None:
        """Hide the autocomplete popup."""
        self.popup.withdraw()
        self.listbox_visible = False

    def move_down(self, _: tk.Event) -> str:
        """Highlight next suggestion with ↓ key."""
        if self.listbox_visible and self.listbox.size() > 0:
            self.lb_index = (self.lb_index + 1) % self.listbox.size()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.lb_index)
            self.listbox.activate(self.lb_index)
        return "break"

    def move_up(self, _: tk.Event) -> str:
        """Highlight previous suggestion with ↑ key."""
        if self.listbox_visible and self.listbox.size() > 0:
            self.lb_index = (self.lb_index - 1) % self.listbox.size()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.lb_index)
            self.listbox.activate(self.lb_index)
        return "break"

    def select_item(self, _: tk.Event) -> str:
        """Apply selected suggestion on Enter key."""
        if self.listbox_visible and self.listbox.size() > 0:
            self.select_index(self.lb_index)
        return "break"

    def select_index(self, index: int) -> None:
        """
        Set Entry text to the value selected from the popup.

        Args:
            index (int): Index of the selected item in listbox.
        """
        try:
            value = self.listbox.get(index)
            self.var.set(value)
            self.icursor(tk.END)
        except tk.TclError:
            pass
        self.hide_list()
        self._user_typing = False

    def on_listbox_click(self, event: tk.Event) -> str:
        """Mouse click on suggestion: select it."""
        index = self.listbox.nearest(event.y)
        self.select_index(index)
        return "break"

    def on_listbox_motion(self, event: tk.Event) -> None:
        """Mouse hover: highlight the suggestion under cursor."""
        index = self.listbox.nearest(event.y)
        if index != self.lb_index:
            self.lb_index = index
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.activate(index)

    def set(self, value: str) -> None:
        """
        Set Entry text programmatically without triggering suggestions.

        Args:
            value (str): The text to insert into the Entry.
        """
        self.var.set(value)
        self._user_typing = False

    def set_completion_list(self, values: List[str]) -> None:
        """
        Update the list of suggestions.

        Args:
            values (List[str]): New list of suggestions.
        """
        self.completevalues = values
