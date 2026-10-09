from pathlib import Path
import re


def main() -> None:
    log_path = Path(__file__).parent / "r1.log"
    if not log_path.exists():
        with open(log_path, "w") as temp:
            temp.write("Sample data\n\nProduct name is:pA Cost is:4565\n\n")

    with open(log_path, "r") as fobj:
        for line in fobj:
            stripped_line = line.strip()
            # Ignore empty lines using regex pattern
            if re.search("^$", stripped_line):
                continue
            print(stripped_line)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates regular expression pattern matching using re.search('^$', ...) to filter out
empty lines while iterating through file records.
"""
