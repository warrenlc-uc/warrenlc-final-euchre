import sqlite3

DATABASE = "euchre.db"

TABLES = [
    "Card",
    "Player",
    "Game",
    "GamePlayer",
    "Round",
    "Trick",
    "CardPlay"
]


def sql_value(value):

    if value is None:
        return "NULL"

    if isinstance(value, str):
        return "'" + value.replace("'", "''") + "'"

    return str(value)


connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

with open("inserts.sql", "w") as file:

    for table in TABLES:
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        for row in rows:
            values = ", ".join(
                sql_value(value)
                for value in row
            )

            file.write(
                f"INSERT INTO {table} VALUES ({values});\n"
            )

        file.write("\n")

connection.close()