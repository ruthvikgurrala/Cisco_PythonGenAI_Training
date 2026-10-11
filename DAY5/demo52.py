import threading
import time


def task(name: str) -> None:
    print(f"{name} started")
    time.sleep(1)
    print(f"{name} completed")


def main() -> None:
    start_time = time.perf_counter()

    t1 = threading.Thread(target=task, args=("Task - 1",))
    t2 = threading.Thread(target=task, args=("Task - 2",))
    t3 = threading.Thread(target=task, args=("Task - 3",))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    end_time = time.perf_counter()
    print(f"Total time:{end_time - start_time:.2f} secs")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates multithreading in Python using threading.Thread, initiating concurrent tasks with .start(),
synchronizing execution with .join(), and measuring performance speedup.
"""