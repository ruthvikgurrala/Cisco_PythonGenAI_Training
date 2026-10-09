class Enrollment:
    def __init__(self, name: str, dob: str, place: str) -> None:
        self.name = name
        self.dob = dob
        self.place = place
        print(f"Emp {self.name} enrollment is done")

    def display(self) -> None:
        print(f"About {self.name} details:-")
        print(f"Name:{self.name} DOB:{self.dob} Place:{self.place}")


def main() -> None:
    obj1 = Enrollment("Arun", "1st Jan", "City-1")
    obj2 = Enrollment("Leo", "2nd Feb", "City-2")

    obj1.display()
    obj2.display()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates object instantiation using the standard __init__() constructor method to automatically
initialize instance variables upon object creation.
"""