from pathlib import Path
import time


class Vendor:
    def __init__(self, vendor_name: str, vendor_gst: str) -> None:
        self.vendor_name = vendor_name
        self.vendor_gst = vendor_gst
        print(f"Vendor {self.vendor_name} enrollment is done")

    def billing(self, product_name: str, product_qty: int = 0, product_cost: float = 0.0) -> None:
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
    vobj1 = Vendor("Klabs", "GST1234")
    vobj2 = Vendor("Xserver", "GST5593")

    vobj1.billing("pA", 5, 1250)
    time.sleep(0.5)
    vobj2.billing("pB", 2, 435.2)
    time.sleep(0.5)
    vobj1.billing("pB", 4, 250)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates an OOP billing model where class instances perform business logic (tax and total calculations)
and persist structured transaction audit records to a log file.
"""