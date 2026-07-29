import os
import subprocess

class CLI:
    """
    Handles command-line display and input.
    """

    @staticmethod
    def clear():
        """
        Clears terminal output.
        """
        command = "cls" if os.name == "nt" else "clear"
        subprocess.run([command], shell=True if os.name == "nt" else False)

    @staticmethod
    def header(title):
        print()
        print("=" * 40)
        print(title.center(40))
        print("=" * 40)

    @staticmethod
    def pause():
        input("\nPress Enter to continue...")

    @staticmethod
    def get_choice(
        prompt,
        minimum,
        maximum
    ):
        while True:
            try:
                choice = int(input(prompt))
                if minimum <= choice <= maximum:
                    return choice
            except ValueError:
                pass
            print("Invalid selection.")



    @staticmethod
    def show_players(players):
        CLI.header("Players")
        if not players:
            print("No players found.")
            return

        for player in players:
            print(
                f"{player[0]} - {player[1]}",
                "(CPU)"
                if player[2]
                else "(Human)"
            )