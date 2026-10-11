from concurrent.futures import ThreadPoolExecutor
import time


def task(name: str) -> str:
    print(f"{name} started")
    time.sleep(1)
    print(f"{name} Completed")
    return f"{name} finished"


def main() -> None:
    with ThreadPoolExecutor(max_workers=3) as executor:
        f1 = executor.submit(task, "Task - 1")
        f2 = executor.submit(task, "Task - 2")
        f3 = executor.submit(task, "Task - 3")

        print(f1.result())
        print(f2.result())
        print(f3.result())

    print("All tasks are completed")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates high-level asynchronous concurrency using concurrent.futures.ThreadPoolExecutor,
submitting worker tasks, and retrieving future results with .result().
"""