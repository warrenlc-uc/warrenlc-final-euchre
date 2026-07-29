from ui.cli import CLI
from classes.game import Game

class GameEngine:
    """
    Controls the flow of a Euchre game.
    """
    def __init__(
            self,
            players,
            team0,
            team1,
            game_repo
        ):
            self.game_repo = game_repo
            game_id = game_repo.create_game()
            self.players = players
            self.game = Game(
                game_id,
                team0,
                team1,
                players
            )
    
            for seat, player in enumerate(players):
                game_repo.add_player(
                    game_id,
                    player.player_id,
                    player.team,
                    seat
                )

    def start(self):
        print("\nStarting Euchre!")
        CLI.pause()

        while True:
            CLI.clear()
            self.show_round_start()
            self.select_trump()
            CLI.pause()
            self.play_round()
            CLI.pause()
            self.score_round()
            CLI.pause()

    def show_round_start(self):
        """
        Displays information for the round.
        """
        CLI.header("NEW ROUND")

    def select_trump(self):
        """
        Implements Euchre bidding.

        Round 1:
        Order up the face card.

        Round 2:
        Pick another suit.

        Stick the dealer:
        Dealer must choose.
        """
        CLI.header("SELECT TRUMP")

    def play_round(self):
        """
        Completes a single round of play.
        """
        CLI.header("PLAY HERE")

    def score_round(self):
        """
        Displays round results and updates score.
        """
        CLI.header("ROUND STATISTICS")