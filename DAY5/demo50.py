import re


def main() -> None:
    disk_sizes: list[str] = ["120GB", "500GB", "GB200", "150Gb", "300gb", "400"]

    total_size: int = 0
    for item in disk_sizes:
        numeric_part = re.sub(r"[A-Za-z]", "", item)
        total_size += int(numeric_part)

    print(f"Sum of {disk_sizes} disk size is:{total_size} GB\n")

    # List comprehension extracting numerical digits
    extracted_sizes = [re.sub(r"[A-Za-z]", "", item) for item in disk_sizes]
    print(extracted_sizes)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates stripping alphabetical characters using regex pattern replacement (re.sub('[A-Za-z]', '')),
aggregating integer sums, and employing list comprehensions for batch string transformations.
"""