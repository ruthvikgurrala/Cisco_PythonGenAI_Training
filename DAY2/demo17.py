import pprint


def main() -> None:
    employee_data: dict = {}

    employee_data["eid"] = [101, 102, 103, 104]
    employee_data["ename"] = ["john", "ram", "raju", "bibu"]
    employee_data["edept"] = ["sales", "prod", "hr", "sales"]
    employee_data["dob"] = {
        "DOB": [
            {"DOB": "1st Jan"},
            {"DOB": "2nd Jan"},
            {"DOB": "3rd Jan"},
            {"DOB": "4th Jan"},
        ]
    }

    pprint.pprint(employee_data)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates constructing nested collections (dictionaries containing lists, nested dictionaries,
and lists of dictionaries) and inspecting complex structures cleanly using pprint.
"""
