import sys


def calculate_sum(first_number: int, second_number: int) -> int:
    return first_number + second_number


def main() -> None:
    print("=== Python Runtime Environment ===")
    print(f"Interpreter Version: {sys.version}\n")

    print("Welcome to Python programming!")
    print("")

    result = calculate_sum(15, 25)
    print(f"Calculation Result (15 + 25): {result}")

    print("End of the line")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates checking the Python runtime environment version using sys.version,
defines a typed function to compute the sum of two integers, and outputs basic messages.
"""