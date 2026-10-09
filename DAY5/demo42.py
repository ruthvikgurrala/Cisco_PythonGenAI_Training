import sys


def main() -> None:
    # 1. Multiple specific except blocks
    try:
        fobj = open("invalidFile", "r")
    except PermissionError as eobj:
        print("This is 1st Except block")
        print(eobj)
    except FileNotFoundError as eobj:
        print("This is 2nd Exception block")
        print(eobj)

    # 2. General Exception capture
    try:
        fobj = open("InvalidFile", "r")
    except Exception as eobj:
        print(eobj)

    print("")

    # 3. Exception inspection via sys.exc_info()
    try:
        fobj = open("InvalidFile", "r")
    except Exception:
        print(sys.exc_info())


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates multi-branch exception handling: targeting specific exception types (PermissionError,
FileNotFoundError), fallback to base Exception, and extracting traceback info with sys.exc_info().
"""
