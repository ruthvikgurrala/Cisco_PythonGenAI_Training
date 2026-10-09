from functools import reduce
from pathlib import Path


def calculate_imperative(csv_lines: list[str]) -> int:
    total = 0
    for line in csv_lines:
        if "sales" in line:
            parts = line.strip().split(",")
            total += int(parts[-1])
    return total


def calculate_functional(csv_lines: list[str]) -> int:
    sales_lines = filter(lambda line: "sales" in line, csv_lines)
    costs = map(lambda line: int(line.strip().split(",")[-1]), sales_lines)
    return reduce(lambda a, b: a + b, costs, 0)


def main() -> None:
    csv_path = Path(__file__).parent / "emp.csv"
    if not csv_path.exists():
        csv_path = Path("emp.csv")

    with open(csv_path, "r") as fobj:
        lines = fobj.readlines()

    # 1. Imperative loop approach
    total_loop = calculate_imperative(lines)
    print(f"Sum of sales dept emp's cost (Loop): {total_loop}")

    # 2. Functional programming approach (map, filter, reduce)
    total_fp = calculate_functional(lines)
    print(f"Sum of sales dept emp's cost (Functional): {total_fp}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates comparing imperative loop-based data aggregation against functional programming
paradigms using map(), filter(), and functools.reduce() on CSV records.
"""
