class Person:
    def __init__(self, name: str) -> None:
        self.name = name


class Vendor(Person):
    def __init__(self, name: str, vid: str) -> None:
        super().__init__(name)
        self.vid = vid


def main() -> None:
    obj = Vendor("Klabs", "V123")
    print(obj.name)
    print(obj.vid)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates single inheritance where a child class (Vendor) inherits from a parent class (Person)
and invokes the parent constructor using super().__init__().
"""
