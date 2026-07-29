class StatisticsRepository:
    def __init__(self, database):
        self.db = database

    def game_stats(self, player_id):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT
                SUM(
                    CASE
                        WHEN gp.Team is not NULL
                        THEN 1
                        ELSE 0
                    END
                ) AS GamesPlayed,

                SUM(
                    CASE
                        WHEN gp.Team = g.WinningTeam
                        THEN 1
                        ELSE 0
                    END
                ) AS GamesWon

            FROM GamePlayer gp

            JOIN Game g
            ON gp.GameID = g.GameID

            WHERE gp.PlayerID = ?
            """,
            (player_id,)
        )
        return cursor.fetchone()


    def round_stats(self,player_id):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT

                COUNT(
                    CASE
                        WHEN gp.PlayerID = ?
                        THEN 1
                    END
                ) AS RoundsPlayed,

                SUM(
                    CASE
                        WHEN CallerPlayerID = ?
                        THEN 1
                        ELSE 0
                    END
                ) AS Calls,

                SUM(
                    CASE
                        WHEN CallerPlayerID = ?
                        AND CallingTeam = WinningTeam
                        THEN 1
                        ELSE 0
                    END
                ) AS SuccessfulCalls,

                SUM(
                    CASE
                        WHEN LonePlayerID = ?
                        THEN 1
                        ELSE 0
                    END
                ) AS LoneHands,

                SUM(
                    CASE
                        WHEN LonePlayerID = ?
                        AND PointsAwarded = 4
                        THEN 1
                        ELSE 0
                    END
                ) AS LoneMarches

            FROM Round r

            JOIN GamePlayer gp
            ON r.GameID = gp.GameID

            WHERE gp.PlayerID = ?
            """,
            (
                player_id,
                player_id,
                player_id,
                player_id,
                player_id,
                player_id
            )
        )
        return cursor.fetchone()


    def trick_stats(self, player_id):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT

                COUNT(*) AS TricksWon

            FROM Trick

            WHERE WinnerPlayerID = ?
            """,
            (player_id,)
        )
        return cursor.fetchone()


    def card_stats(self, player_id):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT

                COUNT(*) AS CardsPlayed

            FROM CardPlay

            WHERE PlayerID = ?
            """,
            (player_id,)
        )
        return cursor.fetchone()


    def favorite_trump(self,player_id):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT

                TrumpSuit,
                COUNT(*) AS TimesCalled

            FROM Round

            WHERE CallerPlayerID = ?

            GROUP BY TrumpSuit

            ORDER BY TimesCalled DESC

            LIMIT 1
            """,
            (player_id,)
        )
        return cursor.fetchone()


    def times_euchred(self,player_id):
        cursor = self.db.cursor()
        cursor.execute(
            """
            SELECT

                COUNT(*)

            FROM Round

            WHERE CallerPlayerID = ?
            AND WinningTeam <> CallingTeam
            """,
            (player_id,)
        )
        return cursor.fetchone()


    def total_statistics(self, player_id):
        """
        Convenience method that returns
        all statistics as a dictionary.
        """
        return {
            "games": self.game_stats(player_id),
            "rounds": self.round_stats(player_id),
            "tricks": self.trick_stats(player_id),
            "cards": self.card_stats(player_id),
            "favorite_trump": self.favorite_trump(player_id),
            "euchred": self.times_euchred(player_id)
        }