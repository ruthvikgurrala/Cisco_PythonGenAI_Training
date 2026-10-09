import logging
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s", force=True)


def get_balance(balance: float) -> Optional[float]:
    try:
        result = 10000 / balance
        logging.info("Balance Calculation is done")
        return result
    except Exception:
        logging.exception("Balance calculation failed")
        return None


def main() -> None:
    print(get_balance(2))
    print(get_balance(0))


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates combining function return values with structured logging, logging successful
operations at INFO level, and capturing division errors with logging.exception().
"""
