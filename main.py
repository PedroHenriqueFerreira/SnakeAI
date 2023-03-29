from tkinter import Tk, Canvas, Frame, Label, StringVar

from game import SnakeGame
from manager import Manager

from config import *


class Main:
    def __init__(self, is_AI: bool = False):
        win = Tk()
        win.config(bg='#222222')
        win.title('Snake Game')

        root = Frame(win, bg="#222222")
        root.pack(expand=1)

        if not is_AI:
            canvas = Canvas(root, width=GAME_SIZE, height=GAME_SIZE)
            canvas.pack(expand=1)

            SnakeGame(canvas, canvas)
        else:
            header = Frame(root, bg="#222222")
            header.grid(row=0, column=0, columnspan=2)

            best_score = StringVar(value=BEST_SCORE_TEXT)
            current_best_score = StringVar(value=CURRENT_BEST_SCORE_TEXT)
            current_alive = StringVar(value=CURRENT_ALIVE_TEXT)
            past_generations = StringVar(value=PAST_GENERATIONS_TEXT)

            for i, text in enumerate([best_score, current_best_score, current_alive, past_generations]):
                Label(
                    header,
                    textvariable=text,
                    font=DEFAULT_FONT,
                    fg=WHITE_COLOR, 
                    bg="#222222"
                ).grid(row=0, column=i, padx=PADDING, pady=PADDING)

            right_column = Frame(root, bg="#222222")
            right_column.grid(row=1, column=1, padx=PADDING)

            best_player_canvas = Canvas(
                right_column,
                width=BEST_GAME_SIZE,
                height=BEST_GAME_SIZE,
                highlightthickness=0
            )
            best_player_canvas.grid(
                row=0, column=0, padx=PADDING, pady=PADDING)

            chart_canvas = Canvas(
                right_column,
                width=CHART_SIZE,
                height=CHART_SIZE,
                highlightthickness=0,
                bg="#222222"
            )
            chart_canvas.grid(row=1, column=0, padx=PADDING, pady=PADDING)
            
            neural_network_canvas = Canvas(
                right_column,
                width=NEURAL_NETWORK_SIZE,
                height=NEURAL_NETWORK_SIZE,
                highlightthickness=0,
                bg="#222222"
            )
            neural_network_canvas.grid(
                row=2, column=0, padx=PADDING, pady=PADDING)

            left_column = Frame(root, bg="#222222")
            left_column.grid(row=1, column=0, padx=PADDING)

            snake_games: list[SnakeGame] = []

            for x in range(GAMES_GRID):
                for y in range(GAMES_GRID):
                    game_canvas = Canvas(
                        left_column,
                        width=GAME_SIZE,
                        height=GAME_SIZE,
                        highlightthickness=0
                    )

                    game_canvas.grid(row=x, column=y, padx=2, pady=2)

                    snake_games.append(
                        SnakeGame(game_canvas, best_player_canvas, True))

            Manager(
                snake_games,
                neural_network_canvas,
                chart_canvas,
                best_player_canvas,
                best_score,
                current_best_score,
                current_alive,
                past_generations
            )

        self.center_win(win)

        win.mainloop()

    def center_win(self, win: Tk):
        win.update()

        win_width = win.winfo_width()
        win_height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        win_x = int((screen_width - win_width) / 2)
        win_y = int((screen_height - win_height) / 2)

        win.geometry(f'{win_width}x{win_height}+{win_x}+{win_y}')


Main(True)
