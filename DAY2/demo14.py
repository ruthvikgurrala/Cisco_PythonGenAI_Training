def main() -> None:
    employees: list[str] = [
        "101,john,sales,1000",
        "102,ram,prod,2000",
        "103,raju,hr,3000",
        "104,bibu,sales,4000",
    ]

    total_salary: int = 0
    for record in employees:
        emp_id, emp_name, emp_dept, emp_cost = record.split(",")
        print(f"Emp Name: {emp_name.title()}\t Emp Dept: {emp_dept.upper()}")
        total_salary += int(emp_cost)

    print(f"\nTotal Salary: {total_salary}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates string splitting with delimiter (split(',')), tuple unpacking,
string case conversions (.title(), .upper()), and accumulator summation over a list.
"""