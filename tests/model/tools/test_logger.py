import pytest
from model.tools.logger import Logger


def test_info_log(caplog):
    with caplog.at_level("INFO"):
        Logger.info("Test info message")
    assert "Test info message" in caplog.text


def test_warning_log(caplog):
    with caplog.at_level("WARNING"):
        Logger.warning("Test warning message")
    assert "Test warning message" in caplog.text


def test_error_log(caplog):
    with caplog.at_level("ERROR"):
        Logger.error("Test error message")
    assert "Test error message" in caplog.text


def test_debug_log(caplog):
    with caplog.at_level("DEBUG"):
        Logger.debug("Test debug message")
    assert "Test debug message" in caplog.text


# Add this for manual run
if __name__ == "__main__":
    pytest.main([__file__])
