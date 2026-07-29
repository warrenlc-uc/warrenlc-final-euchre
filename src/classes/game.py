import random

class Game:
    """
    Represents one complete Euchre game.

    A game continues until one team reaches
    the winning score (normally 10 points).
    """
    def __init__(
        self,
        game_id,
        team0,
        team1,
        players
    ):
        self.game_id = game_id
        self.teams = {
            0: team0,
            1: team1
        }
        self.score = {
            0:0,
            1:0
        }
        self.players = players
        self.rounds = []
        self.dealer_index = random.randrange(0,4)
        self.winner = None

    def current_dealer(self):
        return self.players[self.dealer_index]

    def rotate_dealer(self):
        self.dealer_index = (self.dealer_index + 1) % 4

    def add_round(
        self,
        game_round
    ):
        self.rounds.append(game_round)

    def add_points(
        self,
        team,
        points
    ):
        self.score[team] += points
        self.teams[team].add_point(points)

        if (self.score[team] >= 10):
            self.winner = team

    def is_finished(self):
        return self.winner is not None

    def display_score(self):
        print()
        print("===================")
        print("Score")
        print(f"Team 1: {self.score[0]}")
        print(f"Team 2: {self.score[1]}")
        print("===================")