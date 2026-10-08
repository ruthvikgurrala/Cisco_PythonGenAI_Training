def main() -> None:
    text: str = "  python programming is fun and easy!  "

    print("Original text:", text)
    print("1. strip() ->", text.strip())
    print("2. upper() ->", text.upper())
    print("3. lower() ->", text.lower())
    print("4. replace() ->", text.replace("python", "Python"))
    print("5. split() ->", text.strip().split())
    print("6. find('programming') ->", text.strip().find("programming"))


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates common built-in Python string manipulation methods: strip(), upper(), lower(), replace(), split(), and find().
"""
