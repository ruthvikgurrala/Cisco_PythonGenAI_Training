from pathlib import Path
import sqlite3


def initialize_demo_database(db_path: Path) -> None:
    """Create sample prod table and seed records if not already populated."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS prod (
                id INTEGER PRIMARY KEY,
                name TEXT,
                cost REAL,
                qty INTEGER
            )
            """
        )
        cursor.execute("SELECT COUNT(*) FROM prod")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO prod (id, name, cost, qty) VALUES (?, ?, ?, ?)",
                [
                    (101, "Server-A", 12500.0, 5),
                    (102, "Router-B", 4500.0, 10),
                    (103, "Switch-C", 3200.0, 15),
                ],
            )
        conn.commit()


def main() -> None:
    db_path = Path(__file__).parent / "prod.db"
    initialize_demo_database(db_path)

    try:
        conn = sqlite3.connect(db_path)
    except Exception as eobj:
        print(f"DB Connection failed: {eobj}")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM prod")
        for row in cursor:
            print(row)
    finally:
        conn.close()


if __name__ == "__main__":
    main()

"""
Summary by GenAI:
Demonstrates relational database operations using Python's built-in sqlite3 module: establishing
database connections, creating tables, executing queries, and retrieving row tuples.
"""