class PlayerRepository:
    def __init__(self, database):
        self.db = database

    def create_player(
        self,
        name,
        is_cpu=False
    ):
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO Player
            (
                Name,
                IsCPU
            )
            VALUES
            (?,?)
            """,
            (
                name,
                int(is_cpu)
            )
        )
        self.db.commit()
        return cursor.lastrowid



    def get_players(self):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT
                PlayerID,
                Name,
                IsCPU
            FROM Player
            ORDER BY PlayerID
            """
        )

        return cursor.fetchall()



    def exists(self,name):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM Player
            WHERE Name=?
            """,
            (
                name,
            )
        )

        return (cursor.fetchone()[0]>0)