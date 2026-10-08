import time


def pin_test(pin_candidate: str) -> bool:
    master_pin: int = 1234
    return int(pin_candidate) == master_pin


def main() -> None:
    is_authenticated: bool = False

    for attempt_index in range(3):
        pin_input: str = input("Enter a pin Number: ")
        if pin_test(pin_input):
            print(f"Success - input pin is matched entry date/time: {time.ctime()}")
            is_authenticated = True
            break
        else:
            print(f"Sorry input pin number is not matched: date/time: {time.ctime()}")

    if not is_authenticated:
        print(f"pin is blocked - date/time:{time.ctime()}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates separating validation logic into a helper function with return values,
iterating through fixed attempts using range(3), and handling loop completion guards.
"""