from ui.cli import CLI

class Menus:
    @staticmethod
    def main_menu():
        CLI.header("EUCHRE")
        print("1. Create Player")
        print("2. View Players")
        print("3. Start Game")
        print("4. Statistics")
        print("5. Exit")
        return CLI.get_choice(
            "\nChoice: ",
            1,
            5
        )