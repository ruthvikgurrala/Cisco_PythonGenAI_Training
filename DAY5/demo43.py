class InsufficientBalanceError(Exception):
    """Custom exception raised when an account withdrawal exceeds available balance."""
    pass


def main() -> None:
    # 1. Raising a built-in exception conditionally
    try:
        n = input("Enter n Value: ")
        if int(n) > 100:
            raise ValueError("n value is above 100")
    except Exception as e:
        print(e)

    # 2. Defining and raising a custom user-defined exception
    balance = 1000
    withdraw = 1500
    try:
        if withdraw > balance:
            raise InsufficientBalanceError("Insufficient account balance")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates explicitly raising built-in exceptions (raise ValueError) and creating custom
user-defined exception classes inheriting from Exception to handle domain-specific errors.
"""