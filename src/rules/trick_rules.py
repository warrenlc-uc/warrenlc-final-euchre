class TrickRules:
    """
    Contains Euchre trick evaluation rules.
    """
    @staticmethod
    def card_strength(
        card,
        trump
    ):
        suit = card.get_effective_suit(trump)

        # Highest cards in Euchre
        if (
            card.rank == "J"
            and card.suit == trump
        ):
            return 100


        if (
            card.rank == "J"
            and suit == trump
        ):
            return 90


        if suit == trump:

            values = {
                "A":80,
                "K":70,
                "Q":60,
                "10":50,
                "9":40
            }

            return values[card.rank]


        values = {
            "A":30,
            "K":20,
            "Q":10,
            "J":5,
            "10":4,
            "9":3
        }


        return values[card.rank]



    @staticmethod
    def determine_winner(
        plays,
        trump
    ):

        lead = plays[0]["card"].get_effective_suit(trump)
        winning_play = None
        winning_strength = -1
        for play in plays:
            card = play["card"]
            effective = card.get_effective_suit(trump)

            # Cannot win if off suit
            if (
                effective != trump
                and effective != lead
            ):
                continue

            strength = TrickRules.card_strength(
                card,
                trump
            )

            if strength > winning_strength:
                winning_strength = strength
                winning_play = play
                
        return winning_play["player"]