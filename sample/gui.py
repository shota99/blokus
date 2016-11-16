from tkinter import *
import numpy as np

from blokus.board import *
from blokus.player import RandomPlayer
from blokus.game import Game
from player  import CPlayer

def getPoints(x, y):
    return ((y - 1) * 30 +20, (x - 1) * 30 + 20)

def putDown(canvas, x, y, color):
    i, j = getPoints(x, y)
    canvas.create_rectangle(i + 1, j + 1,  i + 30, j + 30, fill = color)

def drawLines(canvas):
    for i in range(20):
        x = i * 30
        canvas.create_line(x+20, 20,   x+20, 620)
        canvas.create_line(20, x+20, 620, x+20  )

def drawText(canvas):
    numerals="0123456789abcdefghij"
    for i in range(20):
        canvas.create_text( i*30+35, 10, text=numerals[i], font=('FixedSys',16) )
        canvas.create_text( 10, i*30+40, text=numerals[i], font=('FixedSys',16) )
        canvas.create_rectangle(20, 621, 620, 640, fill = 'lightgray')

root = Tk()
root.title("Blokus")
root.geometry("640x700")
root.resizable(width=FALSE, height=FALSE)

canvas = Canvas(root, width = 625, height = 650)
canvas.create_rectangle(20, 20, 620, 620, fill = 'gray')
canvas.place(x=10, y=10)

drawLines(canvas)
drawText(canvas)

players = [RandomPlayer(), RandomPlayer(), RandomPlayer(), RandomPlayer()]

g = Game(players)

def command():
    drawLines(canvas)
    drawText(canvas)
    if not g.isOver():
        g.step()

    b = g.board.board
    color = {R:'red', B:'blue', G:'green', Y:'yellow', Empty:'gray'}
    for (x, y), t in np.ndenumerate(g.board.board):
        putDown(canvas, x + 1, y + 1, color[b[x][y]])

    sco = g.calScores()
    if g.isOver():
       sco.append( "Passed all players!" )
       canvas.create_text( 300, 630, text=sco, font=('FixedSys',16) )
    else:
       canvas.create_text( 300, 630, text=sco, font=('FixedSys',16) )

def keyquit(e):
    exit()

def keyright(e):
    command()

Button(root, text = 'Next', command=command).pack( side = BOTTOM )
root.bind('<Key-Right>', keyright)
root.bind('q',           keyquit )
root.mainloop()
