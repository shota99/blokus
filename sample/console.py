from blokus.game import Game
from blokus.player import RandomPlayer
from player import CPlayer

players = [CPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]

g = Game(players)

while not g.isOver():
    g.step()
    #print(g)
    #print()

print(g.calScores())
