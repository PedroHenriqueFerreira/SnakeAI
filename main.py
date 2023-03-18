from tkinter import Tk, Canvas, Frame, Label, StringVar

from config import RECORD_SCORE_TEXT, BEST_SCORE_TEXT, CURRENT_ALIVE_TEXT, GENERATION_TEXT
from config import CANVAS_SIZE, WINDOW_GRID_X, WINDOW_GRID_Y, FONT_CONFIG, TEXT_PADDING
from config import DARK_COLOR

from snake_game import SnakeGame
from manager import Manager

class Main:
    def __init__(self):
        win = Tk()
        win.title('Snake Game')

        root = Frame(win)
        root.pack(expand=1)

        header = Frame(root)
        header.grid(row=0, column=0)

        record_score = StringVar(value=RECORD_SCORE_TEXT)
        best_score = StringVar(value=BEST_SCORE_TEXT)
        current_alive = StringVar(value=CURRENT_ALIVE_TEXT)
        current_generation = StringVar(value=GENERATION_TEXT)

        for i, text in enumerate([record_score, best_score, current_alive, current_generation]):
            Label(header, textvariable=text, font=FONT_CONFIG, padx=TEXT_PADDING, fg=DARK_COLOR).grid(row=0, column=i)
        
        main = Frame(
            root,
            width=CANVAS_SIZE * WINDOW_GRID_X,
            height=CANVAS_SIZE * WINDOW_GRID_Y
        )
        main.grid(row=1, column=0)

        snake_games: list[SnakeGame] = []

        for x in range(WINDOW_GRID_X):
            for y in range(WINDOW_GRID_Y):
                canvas = Canvas(main, width=CANVAS_SIZE, height=CANVAS_SIZE)
                canvas.grid(row=x, column=y, padx=0, pady=0)

                snake_games.append(SnakeGame(win, canvas, True))

        Manager(snake_games, record_score, best_score, current_alive, current_generation)

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
