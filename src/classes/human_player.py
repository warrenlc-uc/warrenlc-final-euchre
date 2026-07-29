from classes.player import Player

class HumanPlayer(Player):
    """
    Human controlled Euchre player.
    """

    def __init__(
        self,
        player_id,
        name
    ):
        super().__init__(
            player_id,
            name,
            False
        )


    def order_up(
        self,
        up_card
    ):
        """
        First round bidding.

        Player chooses whether to
        order dealer to pick up.
        """
        print()
        self.show_hand()
        while True:
            choice = input("Order up? (y/n): ").lower()
            if choice == "y":
                print(f"{self.name}: Order up")
                return True
            if choice == "n":
                print(f"{self.name}: Pass")
                return False

    def choose_trump(
        self,
        up_card,
        force = False,
    ):
        """
        Second round bidding.
        """
        print()
        print("Choose trump:")
        suits = [
            "Hearts",
            "Diamonds",
            "Clubs",
            "Spades"
        ]
        if up_card.suit in suits:
            suits.remove(up_card.suit)

        for index, suit in enumerate(suits, start=1):
            print(f"{index}. {suit}")

        if not force:
            print("0. Pass")

        while True:
            try:
                choice = int(input("> "))
                if choice == 0 and not force:
                    print(f"{self.name}: Pass")
                    return None
                if 1 <= choice <= len(suits):
                    selected = suits[choice - 1]
                    print(f"{self.name}: calls {selected}")
                    return selected
            except ValueError:
                pass
            print("Invalid selection.")

    def choose_alone(self, trump):
        while True:
            choice = input("Go alone? (y/n): ").lower()
            if choice == "y":
                print(f"\n{self.name} is going alone!")
                return True
            if choice == "n":
                return False

    def play_card(
        self,
        lead_suit,
        trump
    ):
        """
        Human chooses a card to play.

        Shows the entire hand, but highlights
        legal cards.
        """
        legal_cards = self.get_legal_cards(
            lead_suit,
            trump
        )

        print()
        print("Your hand:")

        for index, card in enumerate(
            self.hand,
            start=1
        ):
            if card in legal_cards:
                marker = "✓"
            else:
                marker = "✗"
            print(f"{index}. {str(card):<25} {marker}")

        while True:
            try:
                choice = int(input("Play card: ")) - 1
                if 0 <= choice < len(self.hand):
                    selected = self.hand[choice]
                    if selected not in legal_cards:
                        print("You must follow suit.")
                        continue

                    self.hand.remove(selected)

                    print(f"{self.name} played {selected}")

                    return selected
            except ValueError:
                pass

            print("Invalid selection.")

    def discard_card(self):
        """
        Dealer chooses a discard.

        The discarded card is not announced.
        """
        print()
        print("Choose a card to discard:")
        self.show_hand()

        while True:
            try:
                choice = int(input("> ")) - 1
                if 0 <= choice < len(self.hand):
                    return self.remove_card(choice)
            except ValueError:
                pass
            print("Invalid card.")