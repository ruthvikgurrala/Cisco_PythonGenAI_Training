def main() -> None:
    employee_login_status: bool = True

    employee_name: str = input("Enter employee name: ")
    employee_age: str = input(f"Enter {employee_name} age: ")
    basic_salary_str: str = input(f"Enter {employee_name} basic salary: ")
    basic_salary: float = float(basic_salary_str)
    tax: float = basic_salary * 0.18
    gross_salary: float = basic_salary + tax
    print(f"""Employee Name:{employee_name}
---------------------------------------
{employee_name} Age is:{employee_age}
---------------------------------------
{employee_name} Basic Salary is:{basic_salary_str}
---------------------------------------
{employee_name} Login Status is:{employee_login_status}
-----------------------------------------
Tax is:{tax}
-----------------------------------------
Total Salary is:{gross_salary}
----------------------------------------""")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates collecting employee details via standard input (input()), calculating an 18% tax and total salary, and printing a formatted payroll summary.
"""