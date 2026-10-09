class Teacher:
    def __init__(self, name: str) -> None:
        self.name = name

    def teach(self) -> None:
        print(f"{self.name} is teaching")


class Dept:
    def __init__(self, teacher: Teacher) -> None:
        self.teacher = teacher  # Aggregation: Dept references external Teacher object


def main() -> None:
    teacher1 = Teacher("Ram")
    dept = Dept(teacher1)
    dept.teacher.teach()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates weak aggregation (loose association), where a class maintains a reference to an externally
created object without owning or controlling that object's lifecycle.
"""