from rules.trick_rules import TrickRules

class Trick:
    """
    Represents one trick in a Euchre round.

    A trick consists of four cards played by
    four players. The winner is determined by
    Euchre trick rules.
    """

    def __init__(
        self,
        trick_number
    ):
        self.trick_id = None
        self.trick_number = trick_number
        self.plays = []
        self.winner = None


    def add_play(
        self,
        player,
        card
    ):
        self.plays.append(
            {
                "player": player,
                "card": card
            }
        )


    def is_complete(self):
        return len(self.plays) == 4


    def get_lead_suit(
        self,
        trump
    ):
        if len(self.plays) == 0:
            return None

        return self.plays[0]["card"].get_effective_suit(trump)


    def determine_winner(
        self,
        trump
    ):
        self.winner = TrickRules.determine_winner(
            self.plays,
            trump
        )

        return self.winner


    def display(self):
        print()
        print(f"Trick {self.trick_number + 1}")

        for play in self.plays:
            print(f"{play['player'].name}: {play['card']}")

        if self.winner:
            print(f"Winner: {self.winner.name}")