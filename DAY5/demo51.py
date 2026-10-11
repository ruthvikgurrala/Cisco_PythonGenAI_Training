import time


def task(name: str) -> None:
    print(f"{name} started")
    time.sleep(1)
    print(f"{name} completed")


def main() -> None:
    start_time = time.perf_counter()

    task("Task 1")
    task("Task 2")
    task("Task 3")

    end_time = time.perf_counter()
    print(f"Total time:{end_time - start_time:.2f} secs")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates synchronous, sequential function execution and measures total elapsed runtime
using time.perf_counter().
"""