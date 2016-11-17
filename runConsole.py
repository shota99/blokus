from blokus.game import Game
from blokus.player import RandomPlayer, Anubis, GreedyPlayer
from playerB34 import CPlayerB34

import numpy as np

def plot(game):
    s = ''.join(game.__str__())
    s = s.replace("R", '\x1b[5;30;41m' + '  ' + '\x1b[0m')
    s = s.replace("B", '\x1b[5;30;44m' + '  ' + '\x1b[0m')
    s = s.replace("G", '\x1b[5;30;42m' + '  ' + '\x1b[0m')
    s = s.replace("Y", '\x1b[5;30;43m' + '  ' + '\x1b[0m')
    s = s.replace(".", '\x1b[0;30;47m' + '  ' + '\x1b[0m')
    print(s, "\n")


B34 = CPlayerB34()
# players = [B34, RandomPlayer(), RandomPlayer(), RandomPlayer()]
players = [Anubis(), B34, Anubis(), Anubis()]

g = Game(players)

# for i in range(4):
while not g.isOver():
    g.step()
    plot(g)
score =g.calScores()

print([player.__class__.__name__ for player in players])
print("score: {0}, winner: {1}".format(score, players[np.argmin(score)].__class__.__name__))
print("--------------------------------------------------")


"""
for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')
"""