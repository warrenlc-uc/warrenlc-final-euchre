import random
from classes.player import Player

class CPUPlayer(Player):
    """
    Computer-controlled Euchre player.
    """

    def __init__(
        self,
        player_id,
        name
    ):
        super().__init__(
            player_id,
            name,
            True
        )



    def order_up(
        self,
        up_card
    ):
        """
        Decide whether to order up
        the turned card.
        """
        count = sum(
            1
            for card in self.hand
            if card.suit == up_card.suit
        )
        decision = count >= 3
        print(f"{self.name}: {'Order up' if decision else 'Pass'}")
        return decision



    def choose_trump(
        self,
        up_card,
        force=False
    ):
        """
        Second round trump selection.
        """
        suits = [
            "Hearts",
            "Diamonds",
            "Clubs",
            "Spades"
        ]
        if up_card.suit in suits:
            suits.remove(up_card.suit)
        best_suit = None
        best_count = 0
        for suit in suits:
            count = sum(
                1
                for card in self.hand
                if card.suit == suit
            )
            if count > best_count:
                best_count = count
                best_suit = suit

        if best_count >= 3:
            print(f"{self.name}: calls {best_suit}")
            return best_suit

        if force:
            suit = random.choice(suits)
            print(f"{self.name}: calls {suit}")
            return suit

        print(f"{self.name}: Pass")
        return None


    def choose_alone(
        self,
        trump
    ):
        """
        CPU decides whether to go alone.
        """
        trump_cards = []
        for card in self.hand:
            if card.get_effective_suit(trump) == trump:
                trump_cards.append(card)

        # Check bowers
        has_right = any(
            card.rank == "J"
            and card.get_effective_suit(trump) == trump and card.suit == trump
            for card in self.hand
        )

        has_left = any(
            card.rank == "J"
            and card.suit != card.get_effective_suit(trump)
            for card in self.hand
        )

        # Go alone if it has either bower and at least 4 trump cards
        if has_right or has_left and len(trump_cards) >= 4:
            print(f"\n{self.name} is going alone!")
            return True

        return False



    def play_card(
        self,
        lead_suit,
        trump
    ):
        """
        CPU plays a card.

        Temporary simple AI:
        - Plays a random legal card.
        - Legal play rules will be
          improved next.
        """
        legal_cards = self.get_legal_cards(
            lead_suit,
            trump
        )

        card = random.choice(legal_cards)
        self.hand.remove(card)
        print(f"{self.name} played {card}")
        return card



    def discard_card(self):
        """
        CPU discards lowest card of a Non-Trump Suit.

        The discarded card is not displayed.
        """
        card = self.hand.pop(5)
        return card