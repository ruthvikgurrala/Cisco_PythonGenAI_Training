class Enrollment:
    name: str = ""
    dob: str = ""
    place: str = ""

    def initialize(self, name: str, dob: str, place: str) -> None:
        self.name = name
        self.dob = dob
        self.place = place
        print(f"Emp {self.name} enrollment is done")

    def display(self) -> None:
        print(f"About {self.name} details:-")
        print(f"Name:{self.name} DOB:{self.dob} Place:{self.place}")


def main() -> None:
    obj1 = Enrollment()
    obj1.initialize("Arun", "1st Jan", "City-1")

    obj2 = Enrollment()
    obj2.initialize("Leo", "2nd Feb", "City-2")

    obj1.display()
    obj2.display()

    obj3 = Enrollment()
    obj3.display()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates defining a Python class with class attributes, setting instance state via a custom
initialization method, and calling instance methods on multiple object instances.
"""