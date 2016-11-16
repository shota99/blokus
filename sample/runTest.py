import numpy as np
from blokus.player import RandomPlayer
from blokus.game import Game

players = [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]

scores = [0, 0, 0, 0]

for i in range(1):
    g = Game(players)
    while not g.isOver():
        g.step()
    score = g.calScores()
    for i in range(4):
        scores[i] += score[i]

print(scores)
