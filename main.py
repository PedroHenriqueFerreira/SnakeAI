from tkinter import Tk, Canvas

from config import CANVAS_SIZE, WINDOW_GRID_SIZE
from snake_game import SnakeGame
from manager import Manager

class Main:
    def __init__(self):
        win = Tk()
        win.title('Snake Game')

        games: list[SnakeGame] = []

        for x in range(WINDOW_GRID_SIZE):
            for y in range(WINDOW_GRID_SIZE):
                canvas = Canvas(win, width=CANVAS_SIZE, height=CANVAS_SIZE, borderwidth=0)
                canvas.grid(row=x, column=y, padx=0, pady=0)

                games.append(SnakeGame(win, canvas))

        Manager(games)

        self.center_win(win)

        win.mainloop()

    def center_win(self, win):
        win.update()

        win_width = win.winfo_width()
        win_height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        win_x = int((screen_width - win_width) / 2)
        win_y = int((screen_height - win_height) / 2)

        win.geometry(f'{win_width}x{win_height}+{win_x}+{win_y}')

Main()
