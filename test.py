from game import Game
from tkinter import Canvas, Tk
from config import GAME_SIZE

root = Tk()

canvas = Canvas(root, width=GAME_SIZE, height=GAME_SIZE)
canvas.pack()

Game(canvas, False)

root.mainloop()