import sqlite3
from pathlib import Path

class DatabaseManager:
    """
    Handles SQLite connection management.
    """
    def __init__(self):
        self.root = Path(__file__).resolve().parents[2]
        self.database_path = (self.root/"database"/"euchre.db")
        self.schema_path = (self.root/"database"/"schema.sql")
        self.inserts_path = (self.root/"database"/"inserts.sql")

        self.connection = None

    def connect(self):
        if self.connection is None:
            db_exists = self.database_path.exists()
            if not db_exists:
                self.database_path.parent.mkdir(parents=True, exist_ok=True)

            self.connection = sqlite3.connect(self.database_path)
            self.connection.execute("PRAGMA foreign_keys = ON;")

            if not db_exists:
                with open(self.schema_path, "r") as file:
                    schema = file.read()
                self.connection.executescript(schema)
                self.connection.commit()

                with open(self.inserts_path, "r") as file:
                    inserts = file.read()
                self.connection.executescript(inserts)
                self.connection.commit()
                
        return self.connection

    def cursor(self):
        return self.connect().cursor()

    def commit(self):
        if self.connection:
            self.connection.commit()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def initialize(self, create_new = False):
        """
        Creates a clean database using schema.sql.
        """
        self.close()

        if self.database_path.exists():
            if not create_new: 
                return
            self.database_path.unlink()

        self.connection = sqlite3.connect(
            self.database_path
        )

        self.connection.execute(
            """
            PRAGMA foreign_keys = ON;
            """
        )

        with open(self.schema_path,"r") as file:
            schema = file.read()
        self.connection.executescript(schema)
        self.commit()

        with open(self.inserts_path,"r") as file:
            inserts = file.read()
        self.connection.executescript(inserts)
        self.commit()