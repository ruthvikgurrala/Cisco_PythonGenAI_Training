class Animal:
    def speak(self) -> None:
        print("Animal makes Sound")


class Dog(Animal):
    def speak(self) -> None:
        print("Dog barks")
        super().speak()  # Invoke base class method


def main() -> None:
    dog = Dog()
    dog.speak()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates method overriding in Python where a subclass provides its own implementation of a method
while also invoking the superclass version via super().
"""
