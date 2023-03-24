from game import Game
from tkinter import Canvas, Tk

root = Tk()

canvas = Canvas(root, width=150, height=150)
canvas.pack()

Game(canvas, False)

root.mainloop()