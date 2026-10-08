from pathlib import Path
import time


def pin_test() -> None:
    log_path = Path(__file__).parent / "pin_history.log"
    fobj = open(log_path, "a")

    master_pin: int = 1234
    attempt_count: int = 0
    user_input_pin: int = -1

    while attempt_count < 3:
        raw_input = input("Enter a pin Number: ")
        attempt_count += 1
        user_input_pin = int(raw_input)

        if user_input_pin == master_pin:
            print(f"Success - {attempt_count}")
            fobj.write(f"Success - {attempt_count} pin input date/time:{time.ctime()}\n")
            break
        else:
            fobj.write(f"Failed - user input pin:{raw_input} date/time:{time.ctime()}\n")

    if user_input_pin != master_pin:
        print("Pin is blocked")
        fobj.write(f"Pin is blocked - {time.ctime()}\n")

    fobj.close()


def main() -> None:
    pin_test()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates combining while loop attempt throttling with persistent file logging in append mode ('a'),
tracking security states, and recording timestamped audit logs using time.ctime().
"""