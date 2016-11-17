from blokus.game import Game
from blokus.player import RandomPlayer, Anubis
from playerB34 import CPlayerB34

B34 = CPlayerB34()
# players = [B34, RandomPlayer(), RandomPlayer(), RandomPlayer()]
players = [Anubis(), B34, Anubis(), Anubis()]

g = Game(players)

for i in range(4):
#while not g.isOver():
    g.step()
    print(g)
    print(' ')
    
print(g.calScores())

s = ''.join(g.__str__())
s = s.replace("R", '\x1b[5;30;41m' + '  ' + '\x1b[0m')
s = s.replace("B", '\x1b[5;30;44m' + '  ' + '\x1b[0m')
s = s.replace("G", '\x1b[5;30;42m' + '  ' + '\x1b[0m')
s = s.replace("Y", '\x1b[5;30;45m' + '  ' + '\x1b[0m')
s = s.replace(".", '\x1b[0;30;47m' + '[]' + '\x1b[0m')
print(s)

for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')