from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(
        self,
        player_id,
        name,
        is_cpu=False
    ):
        self.player_id = player_id
        self.name = name
        self.is_cpu = is_cpu

        self.hand = []
        self.team = None
        self.seat = None

    def receive_cards(self, cards):
        self.hand = list(cards)

    def sort_hand(self, trump=None):
        def euchre_sort_key(c):
            # If no trump is called, default to standard suit and value sorting
            if not trump:
                return (c.suit, c.value)
            eff_suit = c.get_effective_suit(trump)
            # Determine card priority status
            is_right_bower = (c.rank == "J" and c.suit == trump)
            is_left_bower = (c.rank == "J" and c.suit != trump and eff_suit == trump)
            is_trump_suit = (eff_suit == trump)
            if is_right_bower:
                priority = 4
            elif is_left_bower:
                priority = 3
            elif is_trump_suit:
                priority = 2
            else:
                priority = 1
            return (priority, eff_suit, c.value)
        self.hand.sort(key=euchre_sort_key, reverse=True)


    def remove_card(self, index):
        return self.hand.pop(index)

    def show_hand(self):
        print(f"{self.name}'s cards:")

        for i, card in enumerate(self.hand):
            print(f"{i+1}. {card}")

    def get_legal_cards(
        self,
        lead_suit,
        trump
    ):
        """
        Returns cards the player is allowed to play.
        """
        # First player can play anything
        if lead_suit is None:
            return self.hand

        playable = []

        for card in self.hand:
            if card.get_effective_suit(trump) == lead_suit:
                playable.append(card)

        # Must follow suit
        if playable:
            return playable

        # Can play anything if unable to follow
        return self.hand

    @abstractmethod
    def play_card(self, lead_suit, trump):
        pass

    @abstractmethod
    def choose_trump(self, up_card):
        pass

    @abstractmethod
    def order_up(self, up_card):
        pass

    @abstractmethod
    def choose_alone(self, trump):
        pass

    def __str__(self):
        return self.name