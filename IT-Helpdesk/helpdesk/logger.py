"""Application logging configuration for HelpDesk Pro."""

import logging
from pathlib import Path

LOGS_DIR = Path("logs")
LOG_FILE = LOGS_DIR / "app.log"


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure application logging with timestamps and file handler.

    Writes logs to logs/app.log and logs to console.
    """
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger("helpdesk")
    root_logger.setLevel(level)

    # Avoid adding duplicate handlers if function called multiple times
    if not root_logger.handlers:
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s (%(module)s:%(lineno)d): %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        # Stream / Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Get a namespaced logger under the helpdesk root."""
    configure_logging()
    return logging.getLogger(f"helpdesk.{name}")
