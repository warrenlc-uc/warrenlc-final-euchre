# Requirements Specification

## Project Information

**Project:** Euchre Game
**Language:** Python
**Database:** SQLite
**Application Type:** CLI --> (Visual Implementation if time permits)
**Programming Paradigm:** Object-Oriented Programming with Python coroutines for turn management

---

# 1. Project Overview

This project is a turn-based Euchre game developed in Python. The application supports local multiplayer and Human vs. CPU gameplay while storing persistent game data in a relational database.

The system demonstrates object-oriented software design, coroutine-based turn management, and relational database interaction. Players can create profiles, play complete games of Euchre, save completed matches, and review historical statistics.

---

# 2. Purpose

The purpose of this project is to:

* Implement a complete turn-based Euchre game.
* Demonstrate object-oriented programming principles.
* Utilize Python coroutines to control game flow.
* Design and implement a relational database.
* Persist player and game information.
* Demonstrate SQL queries and application-level database interaction.

---

# 3. Scope

The system includes:

* Player management
* Local multiplayer
* Human vs. CPU gameplay
* Full Euchre game logic
* Score tracking
* Game history
* Player statistics
* Database persistence
* SQL reporting

The system does not include:

* Online multiplayer
* User authentication
* Network communication

---

# 4. Functional Requirements

## FR-1 Player Management

The system shall allow users to create new player profiles.

**Acceptance Criteria**

* User enters a unique player name.
* Player record is stored in the database.
* Player appears in the player list.

---

## FR-2 View Players

The system shall display all existing player profiles.

**Acceptance Criteria**

* All players are listed.
* Human and CPU players are identified.

---

## FR-3 Start New Game

The system shall allow users to start a new Euchre game.

**Acceptance Criteria**

* User selects game mode.
* Four players are assigned.
* Game record is created.
* Scores begin at zero.

---

## FR-4 Game Mode Selection

The system shall support:

* Local Multiplayer
* Human vs. CPU

**Acceptance Criteria**

* Selected mode initializes correctly.

---

## FR-5 Shuffle Deck

The system shall create and shuffle a standard Euchre deck.

**Acceptance Criteria**

* Deck contains 24 cards.
* Cards are randomized.
* No duplicate cards exist.

---

## FR-6 Deal Cards

The system shall deal five cards to each player.

**Acceptance Criteria**

* Every player receives five cards.
* Remaining cards become the kitty (discarded).

---

## FR-7 Trump Selection

The system shall implement official Euchre trump selection.

**Acceptance Criteria**

* Up card is shown.
* Players may order up or pass.
* Dealer may pick up the card.
* Second round of trump selection is supported.

---

## FR-8 Play Card

The system shall allow players to play legal cards during their turn.

**Acceptance Criteria**

* Only cards in the player's hand can be played.
* Illegal plays are rejected.
* Played card is removed from the hand.

---

## FR-9 Determine Trick Winner

The system shall determine the winner of each trick.

**Acceptance Criteria**

* Trump suit is applied.
* Left and Right Bowers are handled correctly.
* Winning player is identified.

---

## FR-10 Record Trick

The system shall save each completed trick.

**Acceptance Criteria**

* Trick number is stored.
* Winning player is stored.
* Cards played are recorded.

---

## FR-11 Track Score

The system shall maintain team scores.

**Acceptance Criteria**

* Trick totals update correctly.
* Round scores are calculated.
* Current score is displayed.

---

## FR-12 Determine Game Winner

The system shall determine when the game has ended.

**Acceptance Criteria**

* Game ends when a team reaches ten points.
* Winning team is recorded.

---

## FR-13 Save Completed Game

The system shall save completed games.

**Acceptance Criteria**

* Game record exists.
* Players are linked to the game.
* Final score is stored.

---

## FR-14 View Game History

The system shall display previously completed games.

**Acceptance Criteria**

* Previous games are listed.
* Winner is displayed.
* Final score is displayed.
* Date played is displayed.

---

## FR-15 View Player Statistics

The system shall display player statistics.

**Acceptance Criteria**

* Wins displayed.
* Losses displayed.
* Games played displayed.
* Win percentage displayed.

---

## FR-16 Exit Application

The system shall safely exit.

**Acceptance Criteria**

* Database changes are committed.
* Database connection closes.
* Program exits without errors.

---

# 5. Non-Functional Requirements

## NFR-1 Performance

The application shall respond to user input within one second during normal operation.

---

## NFR-2 Reliability

The application shall preserve database integrity throughout gameplay.

---

## NFR-3 Maintainability

The software shall use modular object-oriented design.

---

## NFR-4 Portability

The application shall run on Windows, macOS, and Linux with Python installed.

---

## NFR-5 Usability

The command-line interface shall provide clear prompts and readable output.

---

## NFR-6 Data Integrity

The database shall enforce primary key and foreign key constraints.

---

## NFR-7 Security

Database operations shall use parameterized SQL queries.

---

## NFR-8 Availability

The application shall function without an Internet connection.

---

## NFR-9 Scalability

The database shall support storing thousands of completed games.

---

## NFR-10 Accuracy

The application shall correctly implement official Euchre rules.

---

## NFR-11 Code Quality

The project shall follow Python coding standards and include documentation comments.

---

## NFR-12 Recoverability

Unexpected program termination shall not corrupt existing database records.

---

# 6. Use Cases

## UC-1 Create Player

**Actor:** User

**Preconditions**

* Program is running.

**Main Flow**

1. User selects Create Player.
2. User enters a unique player name.
3. System validates the name.
4. Player is saved.
5. Confirmation is displayed.

**Postconditions**

* Player exists in the database.

---

## UC-2 Start New Game

**Actor:** User

**Preconditions**

* Four player profiles are available.

**Main Flow**

1. User selects New Game.
2. User chooses Local Multiplayer or Human vs. CPU.
3. Players are assigned.
4. Deck is shuffled.
5. Cards are dealt.
6. Game begins.

**Postconditions**

* A new game record is created.

---

## UC-3 Select Trump

**Actor:** Current Player

**Preconditions**

* Cards have been dealt.

**Main Flow**

1. Up card is revealed.
2. Players choose Order Up or Pass.
3. Dealer resolves the first round.
4. If necessary, players choose a trump suit in the second round.

**Postconditions**

* Trump suit is selected.

---

## UC-4 Play Card

**Actor:** Current Player

**Preconditions**

* It is the player's turn.

**Main Flow**

1. Player views hand.
2. Player selects a card.
3. System validates the move.
4. Card is played.

**Postconditions**

* Card is removed from the player's hand.

---

## UC-5 Complete Trick

**Actor:** System

**Preconditions**

* Four cards have been played.

**Main Flow**

1. Determine the winning card.
2. Award the trick to the winning player.
3. Save trick information.

**Postconditions**

* Trick is stored in the database.

---

## UC-6 Finish Game

**Actor:** System

**Preconditions**

* A team reaches ten points.

**Main Flow**

1. Determine the winning team.
2. Save the game.
3. Update player statistics.

**Postconditions**

* Game is marked complete.

---

## UC-7 View Game History

**Actor:** User

**Preconditions**

* At least one completed game exists.

**Main Flow**

1. User selects Game History.
2. System retrieves completed games.
3. History is displayed.

**Postconditions**

* No data is modified.

---

## UC-8 View Player Statistics

**Actor:** User

**Preconditions**

* At least one player exists.

**Main Flow**

1. User selects Statistics.
2. System retrieves player records.
3. Statistics are displayed.

**Postconditions**

* No data is modified.

---

## UC-9 Exit Application

**Actor:** User

**Preconditions**

* Application is running.

**Main Flow**

1. User selects Exit.
2. Pending changes are committed.
3. Database connection closes.
4. Program terminates.

**Postconditions**

* Application exits safely.

---

# 7. Assumptions

* A standard 24-card Euchre deck is used.
* The application is executed locally.
* Each player has a unique name.
* The database is available when the application starts.

---

# 8. Constraints

* The application is implemented in Python.
* Persistent storage uses a relational database.
* Gameplay occurs through a command-line interface.
* No Internet connection is required.
* Multiplayer is limited to local play on a single computer.