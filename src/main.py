from database.database_manager import DatabaseManager
from database.player_repository import PlayerRepository
from database.statistics_repository import StatisticsRepository
from database.game_repository import GameRepository
from database.round_repository import RoundRepository
from database.trick_repository import TrickRepository


from engine.game_engine import GameEngine
from classes.human_player import HumanPlayer
from classes.team import Team
from classes.cpu_player import CPUPlayer
from ui.menus import Menus
from ui.cli import CLI

def main():
    try:
        database = DatabaseManager()

        database.connect()
        database.initialize(create_new=False)

        player_repo = PlayerRepository(database)
        stats_repo = StatisticsRepository(database)
        game_repo = GameRepository(database)
        round_repo = RoundRepository(database)
        trick_repo = TrickRepository(database)


        while True:
            choice = Menus.main_menu()
            if choice == 1:
                name = input("Player name: ")
                if not name.strip():
                    print("Cannot add an empty username.")
                elif player_repo.exists(name):
                    print("Player already exists.")
                else:
                    player_repo.create_player(name)
                    print("Player created.")
            elif choice == 2:
                CLI.show_players(player_repo.get_players())
            elif choice == 3:
                start_game(player_repo, game_repo, round_repo, trick_repo)
            elif choice == 4:
                show_statistics(
                    player_repo,
                    stats_repo
                )
            elif choice == 5:
                database.close()
                break
            CLI.pause()

    except KeyboardInterrupt:
        print("\n\nProgram interrupted.")
    except Exception as error:
        print(f"\nUnexpected error: {error}")
        raise
    finally:
        database.close()
        print("Database connection closed.")


def start_game(
    player_repo,
    game_repo,
    round_repo,
    trick_repo
):
    CLI.header("Starting Game")
    players = player_repo.get_players()
    humans = [p for p in players if not p[2]]

    if len(humans) == 0:
        print("Create a player first.")
        return

    print("Select player:")
    for index, player in enumerate(humans, start=1):
        print(f"{index}. {player[1]}")
    choice = CLI.get_choice("Choice: ", 1, len(humans))
    CLI.clear()
    CLI.header("TEAMS")

    selected = humans[choice - 1]
    human = HumanPlayer(
        selected[0],
        selected[1]
    )

    cpu_ids = []
    for name in [
        "Alice",
        "Bob",
        "Charles"
    ]:
        if player_repo.exists(name):
            for p in player_repo.get_players():
                if p[1] == name:
                    cpu_ids.append(p[0])
        else:
            cpu_ids.append(
                player_repo.create_player(
                    name,
                    True
                )
            )

    cpu1 = CPUPlayer(cpu_ids[0], "Alice")
    cpu2 = CPUPlayer(cpu_ids[1], "Bob")
    cpu3 = CPUPlayer(cpu_ids[2], "Charles")


    players = [human, cpu1, cpu2, cpu3]
    team0 = Team(human, cpu2)
    print(f"Team 1 - {team0}")
    team1 = Team(cpu1, cpu3)
    print(f"Team 2 - {team1}")

    for p in players:
        if p in team0.players:
            p.team_number = 0
            p.team = team0
        else:
            p.team_number = 1
            p.team=team1

    game = GameEngine(
        players,
        team0,
        team1,
        game_repo,
        round_repo,
        trick_repo
    )
    game.start()


def show_statistics(
    player_repo,
    stats_repo
):
    CLI.header( "Player Statistics")
    players = player_repo.get_players()
    humans = [p for p in players if not p[2]]
    if len(humans) == 0:
        print(
            "Create a player first."
        )
        return
    
    print("Select player:")
    for index, player in enumerate(humans, start=1):
        print(f"{index}. {player[1]}")

    choice = CLI.get_choice(
        "Choice: ",
        1,
        len(humans)
    )
    player = humans[choice - 1]

    stats = stats_repo.total_statistics(player[0])
    games = stats["games"]
    rounds = stats["rounds"]
    tricks = stats["tricks"]
    cards = stats["cards"]
    favorite = stats["favorite_trump"]
    euchred = stats["euchred"]

    CLI.header(f"{player[1]}'s Statistics")

    games_played = games[0] or 0
    games_won = games[1] or 0

    win_percent = (
        0
        if games_played == 0
        else 100 * games_won / games_played
    )

    print("Games")
    print("--------------------")
    print(f"Finshed: {games_played}")
    print(f"Won: {games_won}")
    print(f"Win Rate: {win_percent:.1f}%")
    print()

    print("Rounds")
    print("--------------------")
    print(f"Played: {rounds[0] or 0}")
    print(f"Called: {rounds[1] or 0}")
    print(f"Successful Calls: {rounds[2] or 0}")
    print(f"Lone Hands: {rounds[3] or 0}")
    print(f"Lone Marches: {rounds[4] or 0}")
    print(f"Euchred: {euchred[0] or 0}")
    print()

    print("Tricks")
    print("--------------------")
    print(f"Won: {tricks[0] or 0}")
    print()

    print("Cards")
    print("--------------------")
    print(f"Played: {cards[0] or 0}")
    print()

    if favorite:
        print("Favorite Trump")
        print("--------------------")
        print(f"{favorite[0]} ({favorite[1]} calls)")


if __name__ == "__main__":
    main()