class TurnManager:

    def __init__(self, players):
        self.players = players

    def coroutine(self, leader):
        """
        Yields players in clockwise order.

        After all players have acted, the caller
        sends the winner to begin the next trick.

        Works for any amount of players (3 or 4 for our case)
        """
        index = self.players.index(leader)
        while True:
            new_leader = yield self.players[index]
            if new_leader is None:
                index = (index + 1) % len(self.players)
            else:
                index = self.players.index(new_leader)