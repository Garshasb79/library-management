"""
model/tools/logger.py
------------------------
This module provides a simple logger wrapper around Python's built-in logging.
It logs messages to both a file and the console using a unified format.
"""

import logging
import sys
import os


class Logger:
    """
    Logger
    ------
    A static logger class that provides methods for logging informational,
    warning, error, and debug messages.

    Logs are written to:
    - File: log/logging.log
    - Console: Standard output
    """

    log_dir: str = "log"
    log_file: str = os.path.join(log_dir, "logging.log")

    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,  # Enables all levels: DEBUG, INFO, WARNING, ERROR
        format="%(asctime)s - %(filename)s - %(levelname)5s - %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    @classmethod
    def info(cls, message: str) -> None:
        """Log an informational message."""
        logging.info(message)

    @classmethod
    def warning(cls, message: str) -> None:
        """Log a warning message."""
        logging.warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        """Log an error message."""
        logging.error(message)

    @classmethod
    def debug(cls, message: str) -> None:
        """Log a debug message (only shown if logging level is DEBUG)."""
        logging.debug(message)
