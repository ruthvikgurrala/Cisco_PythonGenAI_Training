from pathlib import Path


def file_read() -> None:
    r1_path = Path(__file__).parent / "r1.log"
    if not r1_path.exists():
        with open(r1_path, "w") as temp:
            temp.write("Sample data\nProduct name is:pA Cost is:4565\n")

    fobj = open(r1_path, "r")
    content: str = fobj.read()
    fobj.close()

    print("file contents:-")
    print(content)
    print("End of the function block")


def calculate_sales_cost() -> None:
    total: int = 0
    for value in [10, 20, 30, 40, 50]:
        total += value
    print(f"Sum of cost is:{total}")


def main() -> None:
    print("-- This is Main block")
    file_read()
    print("")
    calculate_sales_cost()
    print("")
    if True:
        file_read()
    print("End of the script")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates defining reusable modular functions (def), reading files within a function,
performing iterative list summation, and executing functions from a main control block.
"""