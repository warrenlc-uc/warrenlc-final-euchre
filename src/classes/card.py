from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    """
    Represents one Euchre card.
    """
    card_id: int
    suit: str
    rank: str
    value: int

    def __str__(self):
        # Found some nice unicode symbols
        symbols = {
            "Hearts": "♥",
            "Diamonds": "♦",
            "Clubs": "♣",
            "Spades": "♠"
        }
        symbol = symbols.get(self.suit, "")

        # ANSI Escape Codes for terminal coloring
        RED = "\033[31m"
        BLUE = "\033[34m"
        RESET = "\033[0m"
        
        # Assign color based on the suit
        if self.suit in ["Hearts", "Diamonds"]:
            color = RED
        else:
            color = BLUE
            
        return f"{color}{symbol} {self.rank}{RESET}"
    
    def get_effective_suit(self, trump):
        """
        Returns the suit this card acts as during a Euchre hand.
        Handles the Left Bower.
        """
        if self.rank == "J":
            # Left bower cases
            if trump == "Hearts" and self.suit == "Diamonds":
                return "Hearts"
            if trump == "Diamonds" and self.suit == "Hearts":
                return "Diamonds"
            if trump == "Clubs" and self.suit == "Spades":
                return "Clubs"
            if trump == "Spades" and self.suit == "Clubs":
                return "Spades"
        return self.suit