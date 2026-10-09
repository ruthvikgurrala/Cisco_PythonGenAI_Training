import logging


def main() -> None:
    logging.basicConfig(level=logging.ERROR, force=True)

    try:
        result = 10 / 0
    except Exception:
        logging.exception("An error occurred")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates using logging.exception() to capture and output detailed traceback context
automatically when an exception is intercepted in a try-except block.
"""