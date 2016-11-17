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

    # print(g, "\n")
    s = ''.join(g.__str__())
    s = s.replace("R", '\x1b[5;30;41m' + '  ' + '\x1b[0m')
    s = s.replace("B", '\x1b[5;30;44m' + '  ' + '\x1b[0m')
    s = s.replace("G", '\x1b[5;30;42m' + '  ' + '\x1b[0m')
    s = s.replace("Y", '\x1b[5;30;43m' + '  ' + '\x1b[0m')
    s = s.replace(".", '\x1b[0;30;47m' + '  ' + '\x1b[0m')
    print(s)
    print([player.__class__.__name__ for player in players])
    print("score: {0}, winner: {1}".format(score, players[np.argmin(score)].__class__.__name__))
    print("--------------------------------------------------")

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

