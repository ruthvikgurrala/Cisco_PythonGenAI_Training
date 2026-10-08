from pathlib import Path


def main() -> None:
    csv_path = Path(__file__).parent / "emp.csv"
    if not csv_path.exists():
        csv_path = Path("emp.csv")

    fobj = open(csv_path, "r")
    lines: list[str] = fobj.readlines()
    fobj.close()

    print(type(lines), len(lines))
    print("")
    print("Display file content:")
    print(lines)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates reading files line-by-line into a Python list of strings using the .readlines() method,
and inspecting the resulting list length and raw line records.
"""