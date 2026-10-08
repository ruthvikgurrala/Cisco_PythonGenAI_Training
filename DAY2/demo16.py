def main() -> None:
    hosts: dict[str, str] = {}
    print(f"Number of elements in the dictionary: {len(hosts)}")

    count: int = 0
    while count < 5:
        hostname = input("Enter a hostname: ")
        ip_address = input("Enter a IP address: ")
        hosts[hostname] = ip_address
        count += 1

    print(f"\nNumber of elements in the dictionary: {len(hosts)}")

    for host in hosts:
        print(f"Hostname: {host}\t IP Address: {hosts[host]}")

    search_host = input("\nEnter a hostname: ")
    if search_host in hosts:
        hosts[search_host] = "127.0.0.1"
    else:
        print(f"Sorry, hostname '{search_host}' does not exist.")
        hosts[search_host] = "127.0.0.1"
        print("Updated dict")

    for host in hosts:
        print(f"\nHostname: {host}\t IP Address: {hosts[host]}")


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates dictionary creation, key-value insertion in a while loop, checking dictionary size with len(),
key traversal with for loop, membership check with 'in', and updating dictionary values.
"""
