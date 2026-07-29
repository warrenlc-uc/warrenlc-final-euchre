class GameRepository:
    def __init__(self, database):
        self.db = database

    def create_game(self):
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO Game
            (
                Team0Score,
                Team1Score
            )
            VALUES
            (
                0,
                0
            )
            """
        )
        self.db.commit()
        return cursor.lastrowid



    def add_player(
        self,
        game_id,
        player_id,
        team,
        seat
    ):
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO GamePlayer
            (
                GameID,
                PlayerID,
                Team,
                SeatPosition
            )
            VALUES
            (?,?,?,?)
            """,
            (
                game_id,
                player_id,
                team,
                seat
            )
        )
        self.db.commit()

    def update_score(
        self,
        game_id,
        team0_score,
        team1_score
    ):
        cursor = self.db.cursor()
        cursor.execute(
            """
            UPDATE Game
            SET
                Team0Score = ?,
                Team1Score = ?
            WHERE GameID = ?
            """,
            (
                team0_score,
                team1_score,
                game_id
            )
        )
        self.db.commit()
        if team0_score >= 10:
            self.finish_game(game_id, 0)
        elif team1_score >= 10:
            self.finish_game(game_id, 1)

    def finish_game(
        self,
        game_id,
        winning_team
    ):
        cursor = self.db.cursor()
        cursor.execute(
            """
            UPDATE Game
            SET WinningTeam = ?
            WHERE GameID = ?
            """,
            (
                winning_team,
                game_id
            )
        )
        self.db.commit()