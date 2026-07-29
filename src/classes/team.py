class Team:
    def __init__(
        self,
        player1,
        player2
    ):
        self.players = [
            player1,
            player2
        ]
        self.score = 0
        self.tricks = 0

    def add_point(
        self,
        points
    ):
        self.score += points

    def add_trick(self):
        self.tricks += 1

    def reset_round(self):
        self.tricks = 0

    def __str__(self):
        return (
            f"{self.players[0]} / {self.players[1]}"
        )