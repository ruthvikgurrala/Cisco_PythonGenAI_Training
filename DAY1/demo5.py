def main() -> None:
    employee_name: str = "Mr.Bruce"
    employee_age: int = 44
    employee_cost: float = 150000.32
    employee_login_status: bool = False

    print(f"""Employee Name: {employee_name}
********************************
Employee Age: {employee_age}
*********************
Employee Cost: {employee_cost}
*********************
Employee Login Status: {employee_login_status}
****************************************""")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates formatting employee profile details into a bordered summary card using a multi-line f-string and asterisk dividers.
"""