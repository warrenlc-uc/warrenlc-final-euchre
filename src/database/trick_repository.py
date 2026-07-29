class TrickRepository:
    """
    Handles database operations for the
    Trick table.
    """

    def __init__(self, database):
        self.db = database

    def create_trick(
        self,
        round_id,
        trick_number
    ):
        """
        Creates a trick before any cards
        have been played.

        Returns the generated TrickID.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO Trick
            (
                RoundID,
                TrickNumber
            )
            VALUES
            (
                ?, ?
            )
            """,
            (
                round_id,
                trick_number
            )
        )
        self.db.commit()
        return cursor.lastrowid


    def finish_trick(
        self,
        trick_id,
        winner_player_id
    ):
        """
        Saves the winner of a completed trick.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            UPDATE Trick
            SET WinnerPlayerID=?
            WHERE TrickID=?
            """,
            (
                winner_player_id,
                trick_id
            )
        )
        self.db.commit()