class CardPlayRepository:
    """
    Handles database operations for the
    CardPlay table.
    """

    def __init__(self, database):
        self.db = database


    def add_play(
        self,
        trick_id,
        player_id,
        card_id,
        play_order
    ):
        """
        Records one card played in a trick.
        """
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO CardPlay
            (
                TrickID,
                PlayerID,
                CardID,
                PlayOrder
            )
            VALUES
            (
                ?, ?, ?, ?
            )
            """,
            (
                trick_id,
                player_id,
                card_id,
                play_order
            )
        )

        self.db.commit()