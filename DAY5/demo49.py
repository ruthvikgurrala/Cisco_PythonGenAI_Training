from pathlib import Path
import re


def main() -> None:
    csv_path = Path(__file__).parent / "emp.csv"
    if not csv_path.exists():
        csv_path = Path(__file__).parent.parent / "DAY3" / "emp.csv"

    with open(csv_path, "r") as fobj:
        for line in fobj:
            if re.search("sales", line, re.IGNORECASE):
                updated_line = re.sub("pune", "HYDERABAD", line)
                if "HYDERABAD" in updated_line:
                    print(updated_line.strip())


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates regular expression search with case-insensitivity (re.I) and pattern substitution
using re.sub() to update delimited CSV records line-by-line.
"""