class Engine:
    def start(self) -> None:
        print("Engine started")


class Car:
    def __init__(self) -> None:
        self.engine_obj = Engine()  # Composition: Car has-an Engine

    def driving(self) -> None:
        self.engine_obj.start()
        print("Car is driving")


def main() -> None:
    car = Car()
    car.driving()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates object composition (tight coupling / 'Has-A' relationship), where an enclosing class
instantiates and manages the lifecycle of an internal component object.
"""