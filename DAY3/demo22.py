from pathlib import Path


def main() -> None:
    output_path = Path(__file__).parent / "r1.log"

    wobj = open(output_path, "w")
    wobj.write("Sample data\n")
    wobj.write("Product name is:pA Cost is:4565\n")

    pname: str = "pB"
    pcost: float = 35523.23
    wobj.write(f"Product name is:{pname} Cost is:{pcost}\n")
    wobj.write("---------------------------------\n")
    wobj.close()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates creating and writing text to a file using open() in write mode ('w'),
formatting dynamic data with f-strings, writing newlines, and properly closing the file handle.
"""