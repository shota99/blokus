import numpy as np
from blokus.game import Game
import importlib
import itertools
import sys

plist = [
    ('playerB34', 'CPlayerB34'), #ここに自分の作ったプレイヤの(ファイル名，クラス名)を設定
    ('blokus.player', 'Anubis'),
    ('blokus.player', 'GreedyPlayer'),
    ('blokus.player', 'RandomPlayer')
    ]

patterns = itertools.permutations(plist, 4)

scores = {}

for (i, l) in enumerate(patterns):
    players = [getattr(importlib.import_module(f), c)() for f, c in l]

    print("start %s" % i)

    g = Game(players)
    while not g.isOver():
        g.step()

    score = g.calScores()
    for i in range(4):
        name = players[i].__class__.__name__
        scores[name] = scores.get(name, 0) + score[i]

for k, v in sorted(scores.items(), key=lambda x: x[1]):
    print(k, v)

