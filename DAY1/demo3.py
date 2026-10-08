def main() -> None:
    dept: str = "sales"

    print(dept)
    print("dept")
    print(type(dept))
    print(type("production"))
    print(type(10))
    print(type(10.0))
    print(type(True), type(False))


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates variable lookup versus string literals, and inspects fundamental Python primitive types (str, int, float, and bool).
"""