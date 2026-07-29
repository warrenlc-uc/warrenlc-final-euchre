## Author

Lincoln Warren

University of Cincinnati

Computer Science Class of 2029

# Euchre Game

A command-line implementation of the classic card game **Euchre** written in Python. The project follows an object-oriented design and uses an SQLite database to persist games, rounds, tricks, card plays, and player statistics.

## Features

- Play against three computer-controlled opponents
- Human vs. CPU gameplay
- Complete Euchre rules
  - Trump selection
  - Stick the dealer
  - Left and right bowers
  - Following suit enforcement
  - Going alone
  - Round and game scoring
- Persistent SQLite database
- Player profiles
- Detailed game history
- Player statistics
- Object-oriented architecture
- Repository pattern for database access

## Project Structure

```
src/
│
├── classes/          # Core game objects
├── database/         # Database manager and repositories
├── engine/           # Game engine and turn manager
├── rules/            # Game rules and scoring
├── ui/               # Menus and command-line interface
├── schema.sql        # Database schema
└── main.py           # Application entry point
```

## Database Design

The application stores all game information in a normalized SQLite database.

Tables include:

- Player
- Game
- GamePlayer
- Round
- Trick
- Card
- CardPlay

This design allows every completed game to be reconstructed from the database while also supporting player statistics.

## Game Flow

1. Create or select a player.
2. Start a new game.
3. Cards are dealt.
4. Players bid for trump.
5. The winning bidder may choose to go alone.
6. Five tricks are played.
7. Points are awarded.
8. Play continues until one team reaches 10 points.

## Scoring

| Situation | Points |
|-----------|-------:|
| Calling team wins | 1 |
| Calling team wins all 5 tricks (March) | 2 |
| Calling player goes alone and wins all 5 tricks | 4 |
| Defending team euchres the callers | 2 |

## Statistics

Player statistics include:

- Games played
- Games won
- Win percentage
- Rounds played
- Times called trump
- Successful calls
- Times euchred
- Lone hands
- Lone marches
- Tricks won
- Cards played
- Favorite trump suit (if there is one)

## Technologies Used

- Python
- SQLite
- Object-Oriented Programming
- Command-Line Interface (CLI)

## Running the Project

1. Clone the repository.

```bash
git clone https://github.com/warrenlc-uc/warrenlc-final-euchre.git
```

2. Navigate into the project directory.

```bash
cd warrenlc-euchre-final
```

3. Run the application.

```bash
python3 src/main.py
```

The database is automatically initialized the first time the application runs.
