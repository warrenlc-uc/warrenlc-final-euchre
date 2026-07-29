import random
from classes.card import Card

class Deck:
    # Matches our SQL inserts for IDs
    SUITS = [
        "Hearts",
        "Diamonds",
        "Clubs",
        "Spades"
    ]
    RANKS = [
        ("9", 9),
        ("10", 10),
        ("J", 11),
        ("Q", 12),
        ("K", 13),
        ("A", 14)
    ]

    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        card_id = 1
        for suit in self.SUITS:
            for rank, value in self.RANKS:
                self.cards.append(
                    Card(
                        card_id,
                        suit,
                        rank,
                        value
                    )
                )
                card_id += 1

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        hands = [[] for _ in range(4)]
        for _ in range(5):
            for player in range(4):
                hands[player].append(
                    self.cards.pop()
                )
        kitty = self.cards
        return hands, kitty

    def __len__(self):
        return len(self.cards)