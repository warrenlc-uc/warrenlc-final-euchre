from ui.cli import CLI
from classes.game import Game
from classes.round import Round
from engine.turn_manager import TurnManager
from rules.scoring import Scoring
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
            round_repo,
            trick_repo,
            card_play_repo
        ):
            self.game_repo = game_repo
            self.round_repo = round_repo
            self.trick_repo = trick_repo
            self.card_play_repo = card_play_repo
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

        while not self.game.is_finished():
            CLI.clear()
            dealer = self.game.current_dealer()
            print(f"Dealer: {dealer.name}")

            current_round = Round(dealer, self.players, self.round_repo, self.trick_repo, self.card_play_repo)
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
            self.play_round(current_round)
            self.score_round(current_round)
            self.game.rotate_dealer()
            CLI.pause()
        print(f"\nTeam {self.game.winner} wins!")

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

    def play_round(self, current_round):
        """
        Completes a single round of play.
        """
        active_players = current_round.get_active_players()
        leader = current_round.get_leader()
        turns = TurnManager(active_players).coroutine(leader)
        current_player = next(turns)

        for trick_number in range(5):
            CLI.clear()
            CLI.header(f"TRICK {trick_number + 1}")
            print(f"Trump: {current_round.trump}")
            print()
            winner = current_round.play_trick(
                turns,
                current_player
            )

            current_player = turns.send(winner)
            CLI.pause()

    def score_round(
        self,
        current_round
    ):
        """
        Displays round results and updates score.
        """
        team0_tricks = current_round.team_tricks[0]
        team1_tricks = current_round.team_tricks[1]

        CLI.clear()
        CLI.header("ROUND RESULT")

        if current_round.going_alone:
            print(f"\n{current_round.caller.name} went alone!")

        print()

        print(f"Team 1 tricks: {team0_tricks}/5")
        print(f"Team 2 tricks: {team1_tricks}/5")

        # Determine winner
        caller_team = current_round.caller.team_number
        caller_tricks = current_round.team_tricks[caller_team]

        # Determine who earns the points
        if caller_tricks >= 3:
            winning_team = 1 + caller_team
        else:
            winning_team = 2 - caller_team

        points = Scoring.calculate(
            caller_tricks,
            current_round.going_alone
        )

        print()

        print(f"Team {winning_team} wins the round!")

        if caller_tricks == 5 or caller_tricks == 0:
            print("March! All five tricks won.")

        print()

        print(f"Points earned: +{points}")

        # Update score
        self.game.add_points(
            winning_team - 1,
            points
        )
        self.game_repo.update_score(
            self.game.game_id,
            self.game.score[0],
            self.game.score[1],
        )
        self.round_repo.finish_round(
            current_round.round_id,
            points,
            winning_team - 1
        )

        self.game.display_score()