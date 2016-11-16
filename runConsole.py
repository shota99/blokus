from blokus.game import Game
from blokus.player import RandomPlayer
from playerB34 import CPlayerB34

B34 = CPlayerB34()
O = CPlayerB34()
players = [B34, RandomPlayer(), RandomPlayer(), RandomPlayer()]

g = Game(players)

while not g.isOver():
    g.step()
    print(g)
    print(' ')
    
print(g.calScores())
