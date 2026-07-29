from classes.deck import Deck
from classes.trick import Trick
import time

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
        round_repo,
        trick_repo,
        card_play_repo
    ):
        self.round_id = None
        self.round_repo = round_repo
        self.trick_repo = trick_repo
        self.card_play_repo = card_play_repo
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

    def play_trick(
        self,
        turns,
        current_player
    ):
        """
        Plays one trick.
        """
        trick = Trick(len(self.tricks),)

        trick.trick_id = self.trick_repo.create_trick(
            self.round_id,
            trick.trick_number
        )

        active_players = self.get_active_players()

        for i in range(len(active_players)):
            time.sleep(1)

            player = current_player
            current_player.sort_hand(self.trump)

            card = player.play_card(
                trick.get_lead_suit(self.trump),
                self.trump
            )

            trick.add_play(player, card)

            self.card_play_repo.add_play(
                trick.trick_id,
                player.player_id,
                card.card_id,
                i
            )

            if i < len(active_players)-1:
                current_player = turns.send(None)



        winner = trick.determine_winner(self.trump)
        self.tricks.append(trick)

        self.team_tricks[winner.team_number] += 1
        
        calling_team_tricks = self.team_tricks[self.caller.team_number]
        defending_team_tricks = self.team_tricks[1 - self.caller.team_number]

        self.round_repo.update_round(
            self.round_id,
            calling_team_tricks,
            defending_team_tricks
        )

        self.trick_repo.finish_trick(
            trick.trick_id,
            winner.player_id
        )

        print()
        print(f"Trick winner: {winner.name}")
        return winner