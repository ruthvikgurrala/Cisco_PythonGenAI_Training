def main() -> None:
    app_name: str = input("Enter app name: ")

    if app_name == "flask":
        port = 5000
    elif app_name == "fastAPI":
        port = 8080
    elif app_name == "prometheus":
        port = 9090
    else:
        app_name = "web2.0"
        port = 8000

    print(f"App Name is:{app_name} Running Port Number is:{port}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates multi-branch decision making using if-elif-else to map specific service names (flask, fastAPI, prometheus) to corresponding ports, defaulting to web2.0 on port 8000.
"""
