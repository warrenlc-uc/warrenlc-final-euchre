from ui.cli import CLI
from classes.game import Game
from classes.round import Round
import time

class GameEngine:
    """
    Controls the flow of a Euchre game.
    """
    def __init__(
            self,
            players,
            team0,
            team1,
            game_repo,
            round_repo
        ):
            self.game_repo = game_repo
            self.round_repo = round_repo
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
                    player.team_number,
                    seat
                )

    def start(self):
        print("\nStarting Euchre!")
        CLI.pause()

        while True:
            CLI.clear()
            dealer = self.game.current_dealer()
            print(f"Dealer: {dealer.name}")

            current_round = Round(dealer, self.players, self.round_repo)
            current_round.deal()
            self.show_round_start(current_round)
            self.select_trump(current_round)
            current_round.round_id = self.round_repo.create_round(
                self.game.game_id,
                len(self.game.rounds),
                current_round.dealer.player_id,
                current_round.caller.player_id,
                current_round.caller.team_number,
                current_round.trump,
                current_round.going_alone,
                current_round.lone_player.player_id if current_round.lone_player else None
            )
            CLI.pause()
            self.play_round()
            CLI.pause()
            self.score_round()
            CLI.pause()

    def show_round_start(self, current_round):
        """
        Displays information for the round.
        """
        CLI.clear()
        CLI.header("NEW ROUND")
        print(f"\nDealer: {current_round.dealer.name}")
        print(f"Up Card: {current_round.up_card}\n")

        for player in self.players:
            if not player.is_cpu:
                player.show_hand()

        CLI.pause()

    def select_trump(self, current_round):
        """
        Implements Euchre bidding.

        Round 1:
        Order up the face card.

        Round 2:
        Pick another suit.

        Stick the dealer:
        Dealer must choose.
        """
        order = current_round.get_order()
        CLI.clear()
        CLI.header("TRUMP SELECTION")
        print(f"\nDealer: {current_round.dealer.name}")
        print("\nBidding order:")
        for player in order:
            print(f"- {player.name}")
        print(f"\nUp Card: {current_round.up_card}")

        # -------------------------
        # First round
        # -------------------------
        print("\nFirst round:")

        for player in order:
            if player.is_cpu:
                time.sleep(1)
            decision = player.order_up(current_round.up_card)
            if decision:
                current_round.trump = (current_round.up_card.suit)
                current_round.caller = player
                if player.choose_alone(current_round.trump):
                    current_round.set_lone_player(player)
                current_round.dealer_pickup()
                return True

        # -------------------------
        # Second round
        # -------------------------
        time.sleep(1)
        print("\nSecond round:")
        for player in order[:-1]:
            if player.is_cpu:
                time.sleep(1)
            suit = player.choose_trump(current_round.up_card)
            if suit:
                current_round.trump = suit
                current_round.caller = player
                if player.choose_alone(current_round.trump):
                    current_round.set_lone_player(player)
                return True

        # -------------------------
        # Stick the dealer
        # -------------------------
        time.sleep(1)
        dealer = current_round.dealer
        print("\nStick the dealer rule.")
        print(f"{dealer.name} must choose trump.")
        while not suit:
            suit = dealer.choose_trump(current_round.up_card, True)
        current_round.trump = suit
        current_round.caller = dealer
        if dealer.choose_alone(current_round.trump):
            current_round.set_lone_player(dealer)

        return True

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