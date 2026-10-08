def main() -> None:
    hosts: list[str] = []
    print(f"Number of elements in the list: {len(hosts)}")

    count: int = 0
    while count < 5:
        hostname = input("Enter a hostname: ")
        hosts.append(hostname)
        count += 1

    print(f"\nNumber of elements in the list: {len(hosts)}")

    for host in hosts:
        print(host)

    additional_host: str = input("\nEnter a hostname: ")
    if additional_host in hosts:
        hosts[-1] = additional_host
    else:
        hosts.append(additional_host)

    print("\nUpdated list of hostnames:")
    for host in hosts:
        print(host)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates list creation, dynamic appending with a while loop, checking list length with len(),
iterating with a for loop, membership verification using the 'in' operator, and list indexing.
"""