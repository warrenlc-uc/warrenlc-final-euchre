class RoundRepository:
    """
    Handles database operations for the
    Round table.
    """
    def __init__(self, database):
        self.db = database

    def create_round(
        self,
        game_id,
        round_number,
        dealer_player_id,
        caller_player_id,
        calling_team,
        trump_suit,
        going_alone=False,
        lone_player_id=None
    ):
        """
        Inserts a completed bidding phase into
        the Round table.

        Returns the generated RoundID.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO Round
            (
                GameID,
                RoundNumber,
                DealerPlayerID,
                CallerPlayerID,
                CallingTeam,
                GoingAloneFlag,
                TrumpSuit,
                LonePlayerID
            )
            VALUES
            (
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                game_id,
                round_number,
                dealer_player_id,
                caller_player_id,
                calling_team,
                int(going_alone),
                trump_suit,
                lone_player_id
            )
        )
        self.db.commit()
        return cursor.lastrowid

    def update_round(
        self,
        round_id,
        calling_team_tricks,
        defending_team_tricks
    ):
        """
        Updates the current trick totals after
        every completed trick.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            UPDATE Round
            SET
                CallingTeamTricks=?,
                DefendingTeamTricks=?
            WHERE RoundID=?
            """,
            (
                calling_team_tricks,
                defending_team_tricks,
                round_id
            )
        )
        self.db.commit()

    def finish_round(
        self,
        round_id,
        points_awarded,
        winning_team
    ):
        """
        Saves the final outcome of the round.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            UPDATE Round
            SET
                PointsAwarded=?,
                WinningTeam=?
            WHERE RoundID=?
            """,
            (
                points_awarded,
                winning_team,
                round_id
            )
        )
        self.db.commit()