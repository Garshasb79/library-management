"""
view/component.__init__.py
---------------------
This module serves as a centralized import hub for reusable GUI components used across the application.

It exposes the following classes:
- LabelAndEntry: A labeled entry field (supports str/int).
- LabelAndCombo: A labeled autocomplete entry field.
- LabelAndDate: A labeled date picker using tkcalendar.
- Table: A generic sortable table view.

Importing from this module simplifies usage:
    from view.component import LabelAndEntry, LabelAndCombo, LabelAndDate, Table
"""

from view.component.label_and_entry import LabelAndEntry, LabelAndCombo, LabelAndDate
from view.component.table import Table
