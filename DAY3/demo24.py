from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).parent
    r1_path = base_dir / "r1.log"
    r3_path = base_dir / "r3.log"
    r4_path = base_dir / "r4.log"

    # Ensure r1.log exists for reading
    if not r1_path.exists():
        with open(r1_path, "w") as temp:
            temp.write("Sample data\nProduct name is:pA Cost is:4565\n")

    # 1. Traditional open() / close() approach
    fobj = open(r1_path, "r")
    wobj = open(r3_path, "w")
    content: str = fobj.read()
    wobj.write(content)
    fobj.close()
    wobj.close()

    # 2. Context manager approach ('with' keyword)
    with open(r1_path, "r") as src_file:
        with open(r4_path, "w") as dest_file:
            lines = src_file.readlines()
            for line in lines:
                dest_file.write(f"data -> {line}")

    print("End of the line")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates file duplication and transformation comparing manual open()/close() methods
against automatic resource management using Python's 'with' statement (context managers).
"""