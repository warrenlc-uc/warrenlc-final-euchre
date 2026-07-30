PRAGMA foreign_keys = ON;


-- =====================================================
-- QUERY 1:
-- Show all players, their team, seat position,
-- and the game they participated in.
--
-- Demonstrates:
-- - JOIN
-- - Relationship between Player, GamePlayer, Game
-- =====================================================

SELECT
    Player.Name AS Player,
    CASE
        WHEN Player.IsCPU = 1 THEN 'CPU'
        ELSE 'Human'
    END AS PlayerType,
    Game.GameID,
    GamePlayer.Team,
    GamePlayer.SeatPosition
FROM Player
JOIN GamePlayer
    ON Player.PlayerID = GamePlayer.PlayerID
JOIN Game
    ON GamePlayer.GameID = Game.GameID
ORDER BY
    Game.GameID,
    GamePlayer.SeatPosition;



-- =====================================================
-- QUERY 2:
-- Show complete trick history:
-- round number, trick number, winner,
-- and every card played for game 1.
--
-- Demonstrates:
-- - Multi-table query
-- - JOIN across 6 tables
-- =====================================================

SELECT
    Round.RoundNumber,
    Trick.TrickNumber,
    Winner.Name AS TrickWinner,
    Player.Name AS PlayedBy,
    Card.Rank,
    Card.Suit,
    CardPlay.PlayOrder,
    Round.TrumpSuit
FROM CardPlay
JOIN Trick
    ON CardPlay.TrickID = Trick.TrickID
JOIN Round
    ON Trick.RoundID = Round.RoundID
JOIN Player
    ON CardPlay.PlayerID = Player.PlayerID
JOIN Player AS Winner
    ON Trick.WinnerPlayerID = Winner.PlayerID
JOIN Card
    ON CardPlay.CardID = Card.CardID
JOIN Game
    ON Round.GameID = Game.GameID
WHERE Game.GameID = 1
ORDER BY
    Game.GameID,
    Round.RoundNumber,
    Trick.TrickNumber,
    CardPlay.PlayOrder;




-- =====================================================
-- QUERY 3:
-- Show player performance:
-- games played, wins, and win percentage.
--
-- Demonstrates:
-- - Aggregate functions
-- - GROUP BY
-- - CASE statements
-- - Business logic
-- =====================================================

SELECT
    Player.Name AS Player,

    COUNT(Game.GameID) AS GamesPlayed,

    SUM(
        CASE
            WHEN Game.WinningTeam is not NULL
            THEN 1
            ELSE 0
        END
    ) AS GamesFinished,

    SUM(
        CASE
            WHEN Game.WinningTeam = GamePlayer.Team
            THEN 1
            ELSE 0
        END
    ) AS Wins,

    ROUND(
        CAST(
            SUM(
                CASE
                    WHEN Game.WinningTeam = GamePlayer.Team
                    THEN 1
                    ELSE 0
                END
            ) AS FLOAT
        )
        /
        SUM(
            CASE
                WHEN Game.WinningTeam is not NULL
                THEN 1
                ELSE 0
            END
        )
        * 100,
        2
    ) AS WinPercentage

FROM Player

JOIN GamePlayer
    ON Player.PlayerID = GamePlayer.PlayerID

JOIN Game
    ON GamePlayer.GameID = Game.GameID

GROUP BY
    Player.PlayerID

ORDER BY
    WinPercentage DESC;