import threading

balance: int = 1000
lock = threading.Lock()


def deposit() -> None:
    global balance
    with lock:
        balance += 500


def withdraw() -> None:
    global balance
    with lock:
        balance -= 200


def main() -> None:
    t1 = threading.Thread(target=deposit)
    t2 = threading.Thread(target=withdraw)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Balance : {balance}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates thread synchronization and race condition prevention using threading.Lock()
within a context manager (with lock:) to guard shared state mutations.
"""
