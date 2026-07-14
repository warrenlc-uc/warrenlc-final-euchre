PRAGMA foreign_keys = ON;

-- ==========================================
-- Player
-- ==========================================

CREATE TABLE Player (
    PlayerID      INTEGER PRIMARY KEY AUTOINCREMENT,
    Name          TEXT NOT NULL UNIQUE,
    IsCPU         INTEGER NOT NULL CHECK (IsCPU IN (0,1))
);

-- ==========================================
-- Card
-- Stores the 24 unique Euchre cards.
-- ==========================================

CREATE TABLE Card (
    CardID        INTEGER PRIMARY KEY AUTOINCREMENT,
    Suit          TEXT NOT NULL,
    Rank          TEXT NOT NULL,
    CardValue     INTEGER NOT NULL,

    UNIQUE (Suit, Rank)
);

-- ==========================================
-- Game
-- Represents one complete game to 10 points.
-- ==========================================

CREATE TABLE Game (
    GameID            INTEGER PRIMARY KEY AUTOINCREMENT,

    DatePlayed        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    WinningTeam       INTEGER CHECK (WinningTeam IN (0,1)),

    Team0Score        INTEGER NOT NULL DEFAULT 0,
    Team1Score        INTEGER NOT NULL DEFAULT 0
);

-- ==========================================
-- GamePlayer
-- Weak entity between Game & Player
-- ==========================================

CREATE TABLE GamePlayer (
    GameID        INTEGER NOT NULL,
    PlayerID      INTEGER NOT NULL,

    Team          INTEGER NOT NULL CHECK (Team IN (0,1)),

    SeatPosition  INTEGER NOT NULL 
                    CHECK (SeatPosition BETWEEN 0 AND 3),

    PRIMARY KEY (GameID, PlayerID),

    FOREIGN KEY (GameID)
        REFERENCES Game(GameID)
        ON DELETE CASCADE,

    FOREIGN KEY (PlayerID)
        REFERENCES Player(PlayerID)
);

-- ==========================================
-- Round
-- Represents one hand (deal).
-- ==========================================

CREATE TABLE Round (
    RoundID                INTEGER PRIMARY KEY AUTOINCREMENT,

    GameID                 INTEGER NOT NULL,

    RoundNumber            INTEGER NOT NULL,

    DealerPlayerID         INTEGER NOT NULL,

    CallerPlayerID         INTEGER NOT NULL,

    CallingTeam            INTEGER NOT NULL
                             CHECK (CallingTeam IN (0,1)),

    GoingAloneFlag         INTEGER NOT NULL DEFAULT 0
                             CHECK (GoingAloneFlag IN (0,1)),

    TrumpSuit              TEXT NOT NULL,

    LonePlayerID           INTEGER,

    CallingTeamTricks      INTEGER NOT NULL DEFAULT 0
                             CHECK (CallingTeamTricks BETWEEN 0 AND 5),

    DefendingTeamTricks    INTEGER NOT NULL DEFAULT 0
                             CHECK (DefendingTeamTricks BETWEEN 0 AND 5),

    PointsAwarded          INTEGER NOT NULL DEFAULT 0
                             CHECK (PointsAwarded IN (0,1,2,4)),

    WinningTeam            INTEGER
                             CHECK (WinningTeam IN (0,1)),

    UNIQUE(GameID, RoundNumber),

    FOREIGN KEY (GameID)
        REFERENCES Game(GameID)
        ON DELETE CASCADE,

    FOREIGN KEY (DealerPlayerID)
        REFERENCES Player(PlayerID),

    FOREIGN KEY (CallerPlayerID)
        REFERENCES Player(PlayerID),

    FOREIGN KEY (LonePlayerID)
        REFERENCES Player(PlayerID)
);

-- ==========================================
-- Trick
-- One of the five tricks in a round.
-- ==========================================

CREATE TABLE Trick (
    TrickID          INTEGER PRIMARY KEY AUTOINCREMENT,

    RoundID          INTEGER NOT NULL,

    TrickNumber      INTEGER NOT NULL
                      CHECK (TrickNumber BETWEEN 0 AND 4),

    WinnerPlayerID   INTEGER NOT NULL,

    FOREIGN KEY (RoundID)
        REFERENCES Round(RoundID)
        ON DELETE CASCADE,

    FOREIGN KEY (WinnerPlayerID)
        REFERENCES Player(PlayerID),

    UNIQUE (RoundID, TrickNumber)
);

-- ==========================================
-- CardPlay
-- Records every card played in every trick.
-- ==========================================

CREATE TABLE CardPlay (
    PlayID          INTEGER PRIMARY KEY AUTOINCREMENT,

    TrickID         INTEGER NOT NULL,

    PlayerID        INTEGER NOT NULL,

    CardID          INTEGER NOT NULL,

    PlayOrder       INTEGER NOT NULL
                    CHECK (PlayOrder BETWEEN 0 AND 3),

    FOREIGN KEY (TrickID)
        REFERENCES Trick(TrickID)
        ON DELETE CASCADE,

    FOREIGN KEY (PlayerID)
        REFERENCES Player(PlayerID),

    FOREIGN KEY (CardID)
        REFERENCES Card(CardID),

    UNIQUE (TrickID, PlayOrder),

    UNIQUE (TrickID, PlayerID),

    UNIQUE (TrickID, CardID)
);