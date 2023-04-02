from tkinter import Tk, Canvas, Frame, Label, StringVar, Misc

from snake_game import SnakeGame
from manager import Manager

from config import *

class Main:
    def __init__(self, is_AI: bool = False):
        self.win = self.create_win()

        main = Frame(self.win, bg=BG_COLOR)
        main.pack(expand=1)

        if not is_AI:
            canvas = self.create_canvas(main, GAME_SIZE, [0, 0])
            SnakeGame(canvas)
        else:
            header = self.create_frame(main, [0, 0])

            record_text, score_text = StringVar(value=RECORD_TEXT), StringVar(value=SCORE_TEXT)
            alive_text, generation_text = StringVar(value=ALIVE_TEXT), StringVar(value=GENERATION_TEXT)

            for i, text in enumerate([record_text, score_text, alive_text, generation_text]):
                self.create_label(header, text, [0, i])

            body = self.create_frame(main, [1, 0])

            games_container = self.create_frame(body, [0, 0])
            snake_games: list[SnakeGame] = []

            for x in range(GAMES_ROW_GRID):
                for y in range(GAMES_COLUMN_GRID):
                    canvas = self.create_canvas(games_container, GAME_SIZE, [x, y])
                    canvas.grid(padx=PADDING / 2, pady=PADDING / 2)

                    snake_games.append(SnakeGame(canvas, True))

            data_container = self.create_frame(body, [0, 1])
            
            best_game_canvas = self.create_canvas(data_container, BEST_GAME_SIZE, [0, 0])            
            chart_canvas = self.create_canvas(data_container, CHART_SIZE, [1, 0])
            neural_network_canvas = self.create_canvas(data_container, NEURAL_NETWORK_SIZE, [2, 0])

            Manager(
                snake_games,
                neural_network_canvas,
                chart_canvas,
                best_game_canvas,
                record_text,
                score_text,
                alive_text,
                generation_text
            )

        self.center_win()
        self.win.mainloop()

    def create_label(self, parent: Misc, text: StringVar, coord: list[int]):
        label = Label(parent, textvariable=text, fg=LIGHT_COLOR, bg=BG_COLOR, font=DEFAULT_FONT)
        label.grid(row=coord[0], column=coord[1], padx=PADDING, pady=PADDING)
        
        return label

    def create_frame(self, parent: Misc, coord: list[int]):
        frame = Frame(parent, bg=BG_COLOR)
        frame.grid(row=coord[0], column=coord[1], padx=PADDING, pady=PADDING)
        
        return frame

    def create_canvas(self, parent: Misc, size: int, coord: list[int]):
        canvas = Canvas(
            parent, 
            width=size, 
            height=size, 
            highlightthickness=0,
            bg=BG_COLOR
        )
        
        canvas.grid(row=coord[0], column=coord[1], padx=PADDING, pady=PADDING)
        
        return canvas

    def create_win(self):        
        win = Tk()
        win.config(bg=BG_COLOR)
        win.title(TITLE)
        
        return win

    def center_win(self):
        self.win.update()

        win_width = self.win.winfo_width()
        win_height = self.win.winfo_height()
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()

        win_x = int((screen_width - win_width) / 2)
        win_y = int((screen_height - win_height) / 2)

        self.win.geometry(f'{win_width}x{win_height}+{win_x}+{win_y}')

Main(True)