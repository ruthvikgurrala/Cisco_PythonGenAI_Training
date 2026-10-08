def main() -> None:
    s: str = "123456789"
    total: int = 0

    for digit_char in s:
        total += int(digit_char)

    print(f"Sum of the digits in string s is:{total}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates string iteration using a for loop, casting each character digit to an integer, and accumulating the sum of all digits.
"""