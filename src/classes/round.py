from classes.deck import Deck

class Round:
    """
    Represents a single Euchre hand.

    Handles:
    - dealing cards
    - dealer
    - up card
    - trump
    - tricks
    - round scoring
    """

    def __init__(
        self,
        dealer,
        players,
        round_repo
    ):
        self.round_id = None
        self.round_repo = round_repo
        self.dealer = dealer
        self.players = players
        self.trump = None
        self.caller = None
        self.going_alone = False
        self.lone_player = None
        self.kitty = []
        self.up_card = None
        self.tricks = []
        self.team_tricks = {
            0: 0,
            1: 0
        }

    def deal(self):
        """
        Shuffle and deal a Euchre hand.
        """
        deck = Deck()
        deck.shuffle()
        hands, kitty = deck.deal()
        self.kitty = kitty
        self.up_card = kitty[0]

        for player, hand in zip(self.players, hands):
            player.receive_cards(hand)
            player.sort_hand()

    def get_order(self):
        """
        Returns bidding order.

        The player left of the dealer
        starts.

        The dealer always goes last.
        """

        dealer_index = self.players.index(self.dealer)
        return [
            self.players[(dealer_index + 1) % 4],
            self.players[(dealer_index + 2) % 4],
            self.players[(dealer_index + 3) % 4],
            self.players[dealer_index]
        ]

    def dealer_pickup(self):
        """
        Dealer takes the up card and
        discards one card.

        The discarded card is private.
        """
        self.dealer.hand.append(self.up_card)
        self.dealer.sort_hand(self.trump)
        self.dealer.discard_card()
        print(f"\n{self.dealer.name} picked up {self.up_card}")

    def set_lone_player(
        self,
        player
    ):
        """
        Sets the caller as going alone.
        """
        self.going_alone = True
        self.lone_player = player

    def get_active_players(self):
        """
        Returns players participating in the hand.

        If someone goes alone, their teammate
        sits out.
        """
        if not self.going_alone:
            return self.players

        partner = self.lone_player.get_partner()

        return [
            player
            for player in self.players
            if player != partner
        ]


    def get_leader(self):
        """
        Finds the next player from the dealer clockwise.
        """
        index = self.players.index(self.dealer)
        return self.players[(index + 1) % 4]

    def play_trick(self):
        """
        Plays one trick.
        """
        pass