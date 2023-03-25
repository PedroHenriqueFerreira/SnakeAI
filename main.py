from tkinter import Tk, Canvas, Frame, Label, StringVar

from game import Game
from manager import Manager

from config import GAMES_HORIZONTAL_GRID, GAMES_VERTICAL_GRID, BEST_SCORE_TEXT, CURRENT_BEST_SCORE_TEXT, CURRENT_ALIVE_TEXT, PAST_GENERATIONS_TEXT, PADDING, GAME_SIZE, FONT_CONFIG, BLACK_COLOR, CHART_SIZE, NEURAL_NETWORK_SIZE, BEST_GAME_SIZE

class Main:
    def __init__(self, is_ai: bool = False):
        win = Tk()
        win.title('Snake Game')

        root = Frame(win)
        root.pack(expand=1)

        if not is_ai:
            canvas = Canvas(root, width=GAME_SIZE, height=GAME_SIZE)
            canvas.pack(expand=1)

            Game(canvas)
        else:
            left_column = Frame(root)
            left_column.grid(row=0, column=0, padx=(0, PADDING))

            best_score = StringVar(value=BEST_SCORE_TEXT)
            current_best_score = StringVar(value=CURRENT_BEST_SCORE_TEXT)
            current_alive = StringVar(value=CURRENT_ALIVE_TEXT)
            past_generations = StringVar(value=PAST_GENERATIONS_TEXT)

            for i, text in enumerate([best_score, current_best_score, current_alive, past_generations]):
                Label(
                    left_column,
                    textvariable=text,
                    font=FONT_CONFIG,
                    fg=BLACK_COLOR
                ).grid(row=i, column=0, pady=(0, PADDING))

            Frame(left_column, height=300).grid(row=4, column=0)

            Label(
                left_column,
                text="Pontuacao x geracao:",
                font=FONT_CONFIG,
                fg=BLACK_COLOR
            ).grid(row=5, column=0, pady=(0, PADDING))

            chart_canvas = Canvas(
                left_column,
                width=CHART_SIZE,
                height=CHART_SIZE,
                highlightthickness=0
            )
            chart_canvas.grid(row=6, column=0)

            center_column = Frame(root)
            center_column.grid(row=0, column=1)

            snake_games: list[Game] = []

            for x in range(GAMES_VERTICAL_GRID):
                for y in range(GAMES_HORIZONTAL_GRID):
                    game_canvas = Canvas(
                        center_column,
                        width=GAME_SIZE,
                        height=GAME_SIZE,
                        highlightthickness=0
                    )

                    game_canvas.grid(row=x, column=y, padx=2, pady=2)

                    snake_games.append(Game(game_canvas, True))

            right_column = Frame(root)
            right_column.grid(row=0, column=2, padx=(PADDING, 0))


            Label(
                right_column,
                text='Melhor rede neural atual:',
                font=FONT_CONFIG,
                fg=BLACK_COLOR
            ).grid(row=0, column=0, pady=PADDING)

            neural_network_canvas = Canvas(
                right_column,
                width=NEURAL_NETWORK_SIZE,
                height=NEURAL_NETWORK_SIZE,
                highlightthickness=0,
            )
            neural_network_canvas.grid(row=1, column=0)

            Label(
                right_column,
                text='Melhor jogo atual:',
                font=FONT_CONFIG,
                fg=BLACK_COLOR
            ).grid(row=2, column=0, pady=PADDING)

            best_player_canvas = Canvas(
                right_column,
                width=BEST_GAME_SIZE,
                height=BEST_GAME_SIZE
            )
            best_player_canvas.grid(row=3, column=0)

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

    def center_win(self, win):
        win.update()

        win_width = win.winfo_width()
        win_height = win.winfo_height()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        win_x = int((screen_width - win_width) / 2)
        win_y = int((screen_height - win_height) / 2)

        win.geometry(f'{win_width}x{win_height}+{win_x}+{win_y}')


Main(True)
