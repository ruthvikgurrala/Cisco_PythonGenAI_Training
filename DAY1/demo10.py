def main() -> None:
    correct_pin: int = 1234
    attempt_count: int = 0
    user_pin: int = -1
    while attempt_count < 3:
        user_pin = int(input("Enter your pin number: "))
        attempt_count += 1

        if user_pin == correct_pin:
            print(f"Pin Number is Valid - count is:{attempt_count}")
            break

    if correct_pin != user_pin:
        print("Pin is blocked")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates a while loop with a counter limit of 3 attempts for ATM PIN validation, breaking early on success or displaying 'Pin is blocked' after 3 failed attempts.
"""
