import numpy as np
from blokus.game   import Game
import importlib
import itertools
import multiprocessing

def game_thread( i, players, queue ):
#    print("start %s" % i)
    g = Game(players)
    while not g.isOver():
        g.step()

    score = g.calScores()
    results = []
    for i in range(4):
        results.append( [ players[i].__class__.__name__, score[i] ] )

    queue.put( results )
    queue.close()


if __name__ == '__main__':

    plist = [
        ('playerB34', 'CPlayerB34'), #ここに自分の作ったプレイヤの(ファイル名，クラス名)を設定
        ('blokus.player', 'Anubis'),
        ('blokus.player', 'GreedyPlayer'),
        ('blokus.player', 'RandomPlayer')
    ]

    patterns = itertools.permutations(plist, 4)

    pid = [0 for i in range(24) ]
    q   = [0 for i in range(24) ]
    for (i, l) in enumerate(patterns):
        players = [getattr(importlib.import_module(f), c)() for f, c in l]

        print("Thread start %s" % i)
        q[i]   = multiprocessing.Queue()
        pid[i] = multiprocessing.Process(target=game_thread, args=(i,players,q[i],))
        pid[i].start()

    scores = {}

    for i in range(len(pid)) :
        result = q[i].get()
        for name, score in result :
            scores[name] = scores.get(name, 0) + score
        pid[i].join()

    for k, v in sorted(scores.items(), key=lambda x: x[1]):
        print(k, v)

