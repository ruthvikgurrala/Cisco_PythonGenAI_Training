from pathlib import Path


def main() -> None:
    csv_path = Path(__file__).parent / "emp.csv"
    if not csv_path.exists():
        csv_path = Path("emp.csv")

    fobj = open(csv_path, "r")
    content: str = fobj.read()
    fobj.close()

    print(type(content), len(content))
    print("")
    print("Display file content:")
    print(content)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates basic file reading using open() in 'r' mode, retrieving the entire text content as a string
via .read(), closing file resources with .close(), and inspecting data length and type.
"""