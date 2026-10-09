import logging
from pathlib import Path


def main() -> None:
    log_path = Path(__file__).parent / "demo.log"

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )

    logging.info("Application process started")
    logging.warning("5 records contains missing email address")
    logging.error("App is critical state")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates Python's logging module: setting up basicConfig with file destination, timestamp formats,
log severity levels (INFO, WARNING, ERROR), and recording log messages.
"""