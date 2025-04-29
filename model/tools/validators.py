"""
model/tools/validators.py
-------------
This module provides input validation functions used throughout the application.

Functions:
- name_validator: Validates first or last names.
- title_validator: Validates books title.
- type_validator: Validates string-based type labels.
- amount_validator: Validates positive integer values.
- time_validator: Parses and validates time objects.
- date_validator: Validates and converts string/date to a datetime.date object.
"""

import re
from datetime import datetime, date


def name_validator(name: str, message: str) -> str:
    """
    Validate that the name contains only letters and spaces (2-30 chars).

    :param name: Input name string.
    :param message: Error message on failure.
    :return: Validated name.
    :raises ValueError: If validation fails.
    """
    if isinstance(name, str) and re.match(r"^[a-zA-Z\s\.]{2,30}$", name):
        return name
    raise ValueError(message)


def title_validator(title: str, message: str) -> str:
    """
    Validate that the title contains only letters, numbers and spaces (2-30 chars).

    :param title: Input title string.
    :param message: Error message on failure.
    :return: Validated title.
    :raises ValueError: If validation fails.
    """
    if isinstance(title, str) and re.match(r"^[a-zA-Z0-9\s]{2,30}$", title):
        return title
    raise ValueError(message)


def type_validator(type_str: str) -> str:
    """
    Validate that a type label contains only letters and spaces (3-30 chars).

    :param type_str: Input type string.
    :return: Validated type string.
    :raises ValueError: If validation fails.
    """
    if isinstance(type_str, str) and re.match(r"^[a-zA-Z\s]{3,30}$", type_str):
        return type_str
    raise ValueError("Invalid type!")


def amount_validator(amount: int, message: str) -> int:
    """
    Validate that the amount is a positive integer.

    :param amount: Input amount.
    :param message: Error message on failure.
    :return: Validated amount.
    :raises ValueError: If validation fails.
    """
    if isinstance(amount, int) and amount > 0:
        return amount
    raise ValueError(message)


def time_validator(time_input) -> datetime.time:
    """
    Parse a datetime object and return its time component.

    :param time_input: Expected to be a datetime instance.
    :return: Extracted time object.
    :raises ValueError: If input is not a datetime.
    """
    if isinstance(time_input, datetime):
        return time_input.time()
    raise ValueError("Invalid time!")


def date_validator(date_input, message: str) -> date:
    """
    Validate and convert a date input (str or datetime.date) to a date object.

    :param date_input: The input date (str or date).
    :param message: Error message on failure.
    :return: datetime.date object.
    :raises ValueError: If input is invalid.
    """
    try:
        if isinstance(date_input, str):
            return datetime.strptime(date_input, "%Y-%m-%d").date()
        elif isinstance(date_input, date):
            return date_input
        else:
            raise ValueError(f"{message} Received: {type(date_input)}")
    except Exception as e:
        raise ValueError(f"Invalid date format! Use YYYY-MM-DD. {e}") from e
