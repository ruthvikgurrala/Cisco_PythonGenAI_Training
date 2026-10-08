import pprint


def main() -> None:
    # 1. Dictionary of Lists
    products_col: dict[str, list] = {
        "id": [101, 102, 103],
        "names": ["pA", "pB", "pC"],
        "cost": [1000, 2000, 3000],
        "Qty": [10, 20, 30],
    }
    pprint.pprint(products_col)

    print("\n")

    # 2. List of Dictionaries
    products_rows: list[dict] = [
        {"id": 101, "names": "pA", "cost": 1000, "Qty": 10},
        {"id": 102, "names": "pB", "cost": 2000, "Qty": 20},
        {"id": 103, "names": "pC", "cost": 3000, "Qty": 30},
    ]
    pprint.pprint(products_rows)

    print("\n")

    # 3. Dictionary of Dictionaries
    products_nested: dict[str, dict] = {
        "id": {"id1": 101, "id2": 102, "id3": 103},
        "names": {"name1": "pA", "name2": "pB", "name3": "pC"},
        "cost": {"cost1": 1000, "cost2": 2000, "cost3": 3000},
        "Qty": {"Qty1": 10, "Qty2": 20, "Qty3": 30},
    }
    pprint.pprint(products_nested)


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates modeling tabular and nested data using three structures:
dictionary of lists, list of dictionaries, and dictionary of dictionaries, visualized with pprint.
"""