from pathlib import Path
import time


class Vendor:
    """Vendor class to manage profile details and transaction billing."""

    def __init__(self, vendor_name: str, vendor_gst: str) -> None:
        """Initialize vendor registration details."""
        self.vendor_name = vendor_name
        self.vendor_gst = vendor_gst
        print(f"Vendor {self.vendor_name} enrollment is done")

    def billing(self, product_name: str, product_qty: int = 0, product_cost: float = 0.0) -> None:
        """Execute product billing computation and record to log."""
        self.product_name = product_name
        self.product_qty = product_qty
        self.product_cost = product_cost
        self.total = self.product_cost * self.product_qty
        self.tax = self.total * 0.18
        self.gross_salary = self.total + self.tax

        log_path = Path(__file__).parent / "vendor_prods.log"
        record = (
            f"{self.vendor_name}\t{self.vendor_gst}\t{self.product_name}\t{self.product_qty}"
            f"\t{self.product_cost}\t{self.total}\t{self.gross_salary}\t{time.ctime()}\n\n"
        )
        with open(log_path, "a") as wobj:
            wobj.write(record)


def main() -> None:
    vendor_instance = Vendor("Klabs", "GST1234")
    vendor_instance.billing("pA", 3, 500.0)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates documenting class and method signatures with docstrings while performing
parameter calculations and persisting log records.
"""
