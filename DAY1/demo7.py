def main() -> None:
    port: str = input("Enter port number: ")
    port_number: int = int(port)

    if port_number > 5000 and port_number < 6000:
        app_name: str = "Flask"
    else:
        app_name: str = "WebApp"

    print(f"App Name is:{app_name} Running Port Number is:{port}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates conditional branching (if-else) to classify a port number: assigns 'Flask' if port is between 5001 and 5999, otherwise assigns 'WebApp'.
"""