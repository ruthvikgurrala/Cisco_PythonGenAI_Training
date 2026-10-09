def calc(first_number: int, second_number: int) -> int:
    """Calculate and return the sum of two numbers."""
    return first_number + second_number


def main() -> None:
    result = calc(10, 20)
    print(f"Result: {result}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates a clean, typed arithmetic utility function (calc) that takes two numbers,
computes their sum, and is targeted for unit testing with pytest.
"""