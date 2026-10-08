def main() -> None:
    app_name: str = input("Enter app name: ")

    service_status: str = "crm application running in flask web app"
    if app_name in service_status:
        port: int = 5000
    else:
        port: int = 8080

    print(f"App Name is:{app_name} Running Port Number is:{port}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates substring membership testing using the 'in' operator to verify if an app name exists within a cluster status string and assigns port 5000 or 8080 accordingly.
"""