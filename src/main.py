from database.database_manager import DatabaseManager
from database.player_repository import PlayerRepository

from ui.menus import Menus
from ui.cli import CLI

def main():
    try:
        database = DatabaseManager()

        database.connect()
        database.initialize(create_new=True)

        player_repo = PlayerRepository(database)

        while True:
            choice = Menus.main_menu()
            if choice == 1:
                name = input("Player name: ")
                if player_repo.exists(name):
                    print("Player already exists.")
                else:
                    player_repo.create_player(name)
                    print("Player created.")
            elif choice == 2:
                CLI.show_players(player_repo.get_players())
            elif choice == 3:
                print("TODO")
            elif choice == 4:
                print("TODO")
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

if __name__ == "__main__":
    main()