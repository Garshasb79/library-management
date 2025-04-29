"""
Test: model/tools/validators.py
-------------------------------
Unit tests for validator functions used throughout the application.
"""

import pytest
from datetime import datetime, date
from model.tools import validators


def test_name_validator_valid():
    assert validators.name_validator("John Doe", "Error") == "John Doe"


def test_name_validator_invalid():
    with pytest.raises(ValueError):
        validators.name_validator("12@", "Invalid name")


def test_type_validator_valid():
    assert validators.type_validator("Student") == "Student"


def test_type_validator_invalid():
    with pytest.raises(ValueError):
        validators.type_validator("123!")


def test_amount_validator_valid():
    assert validators.amount_validator(5, "Error") == 5


def test_amount_validator_invalid():
    with pytest.raises(ValueError):
        validators.amount_validator(0, "Amount must be > 0")


def test_time_validator_valid():
    now = datetime.now()
    result = validators.time_validator(now)
    assert isinstance(result, type(now.time()))


def test_time_validator_invalid():
    with pytest.raises(ValueError):
        validators.time_validator("10:00")


def test_date_validator_str():
    assert validators.date_validator("2024-04-10", "Invalid") == date(2024, 4, 10)


def test_date_validator_date():
    d = date(2024, 4, 10)
    assert validators.date_validator(d, "Invalid") == d


def test_date_validator_invalid():
    with pytest.raises(ValueError):
        validators.date_validator(123, "Invalid")


# Add this for manual run
if __name__ == "__main__":
    pytest.main([__file__])
