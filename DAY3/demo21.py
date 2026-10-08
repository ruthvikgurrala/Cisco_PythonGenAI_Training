from pathlib import Path


def main() -> None:
    csv_path = Path(__file__).parent / "emp.csv"
    if not csv_path.exists():
        csv_path = Path("emp.csv")

    fobj = open(csv_path, "r")
    lines: list[str] = fobj.readlines()
    fobj.close()

    # 1. Print all stripped lines
    for line in lines:
        print(line.strip())

    print("\n")

    # 2. Filter lines containing 'sales'
    for line in lines:
        if "sales" in line:
            print(line.strip())

    print("\n")

    # 3. Parse fields, format display, and accumulate total cost
    total_sales_cost: int = 0
    for line in lines:
        if "sales" in line:
            stripped_line = line.strip()
            emp_id, emp_name, emp_dept, emp_place, emp_cost = stripped_line.split(",")
            total_sales_cost += int(emp_cost)
            print(f"Emp Name is:{emp_name.title()}  \t Working Dept is:{emp_dept.upper()}")

    print("-" * 35)
    print(f"Sum of sales dept emp's cost is:{total_sales_cost}")
    print("-" * 35)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates processing CSV file lines with .readlines(), whitespace removal using .strip(),
string filtering with 'in', field extraction via .split(','), string formatting, and integer accumulation.
"""