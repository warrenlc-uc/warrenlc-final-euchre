import sqlite3
from pathlib import Path
from tabulate import tabulate

DATABASE_PATH = Path("database/euchre.db")
SCHEMA_PATH = Path("database/schema.sql")
INSERTS_PATH = Path("database/inserts.sql")
QUERIES_PATH = Path("database/queries.sql")


def create_database():
    """
    Creates a fresh database and loads schema + sample data.
    """
    # Remove old database for clean testing
    if DATABASE_PATH.exists():
        DATABASE_PATH.unlink()

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign keys
    connection.execute("PRAGMA foreign_keys = ON;")

    print("Creating database schema...")
    with open(SCHEMA_PATH, "r") as file:
        schema = file.read()
    connection.executescript(schema)

    print("Loading sample data...")
    with open(INSERTS_PATH, "r") as file:
        inserts = file.read()
    connection.executescript(inserts)

    connection.commit()
    return connection


def run_queries(connection):
    """
    Executes SQL queries and prints readable output.
    """
    print("\nRunning queries...\n")

    with open(QUERIES_PATH, "r") as file:
        queries = file.read()

    query_list = [
        query.strip()
        for query in queries.split(";")
        if query.strip()
        and not query.strip().upper().startswith("PRAGMA")
    ]

    cursor = connection.cursor()

    descriptions = [
        """
        Shows every player participating in a game, including whether they are
        human or CPU, their team assignment, and seat position.
        """,
        """
        Shows the complete history of played tricks. Displays the round, trick,
        winner, player actions, and cards played. This demonstrates relationships
        across CardPlay, Trick, Round, Player, and Card.
        """,
        """
        Calculates player performance statistics: games played, wins,
        and win percentage.
        """
    ]

    for index, query in enumerate(query_list, start=1):
        print("=" * 80)
        print(f"QUERY {index}")
        print("=" * 80)

        if index <= len(descriptions):
            print("Purpose:")
            print(descriptions[index - 1].strip())
            print()

        print("SQL:")
        print(query)
        print()

        try:
            cursor.execute(query)
            results = cursor.fetchall()

            # Get column names
            columns = [description[0] for description in cursor.description]

            print("Results:")

            if results:
                print(tabulate(
                    results,
                    headers=columns,
                    tablefmt="rounded_outline",
                    stralign="left",
                    numalign="center"
                ))
            else:
                print("No results found.")

            print()

        except sqlite3.Error as error:
            print(f"SQL Error: {error}\n")


def main():
    connection = create_database()

    try:
        run_queries(connection)
    finally:
        connection.close()

    print("Database testing complete.")


if __name__ == "__main__":
    main()