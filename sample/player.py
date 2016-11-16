from blokus.player import Player
from blokus.utils import encodeFourCode

class CPlayer(Player):
    def __init__(self):
        super().__init__()

        self.count = 0
        self.logs = []

    def log(self, player, move):
        self.logs.append((player, move))

    def move(self, board, pieces):
        self.count += 1
        hand = "pass"

        if self.count == 1:
            hand = encodeFourCode(19, 2, 'q', 2)
        elif self.count == 2:
            hand = encodeFourCode(15, 4, 'r', 2)
        elif self.count == 3:
            hand = encodeFourCode(12, 7, 't', 5)

        return hand