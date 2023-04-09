from UI import Tk, Canvas, Frame, Label

from snake_game import SnakeGame
from manager import Manager

from config import *

class Main:
    def __init__(self, is_AI: bool = False):
        win = Tk(TITLE, BG_COLOR, LIGHT_COLOR, DEFAULT_FONT)

        main = Frame(win)

        if not is_AI:
            SnakeGame(Canvas(main, GAME_SIZE, [0, 0], PADDING))
        else:
            header = Frame(main, [0, 0], PADDING)

            labels: list[Label] = []

            for i, text in enumerate([GENERATION_TEXT, RECORD_TEXT, SCORE_TEXT, ALIVE_TEXT]):
                labels.append(Label(header, text, [0, i], PADDING))

            body = Frame(main, [1, 0], PADDING)

            games_container = Frame(body, [0, 0], PADDING)
            snake_games: list[SnakeGame] = []

            for x in range(GAMES_ROW_GRID):
                for y in range(GAMES_COLUMN_GRID):
                    canvas = Canvas(games_container, GAME_SIZE, [x, y], PADDING / 2)

                    snake_games.append(SnakeGame(canvas, True))

            data_container = Frame(body, [0, 1], PADDING)
            
            best_game_canvas = Canvas(data_container, BEST_GAME_SIZE, [0, 0], PADDING)            
            chart_canvas = Canvas(data_container, CHART_SIZE, [1, 0], PADDING)
            neural_network_canvas = Canvas(data_container, NEURAL_NETWORK_SIZE, [2, 0], PADDING)

            Manager(
                snake_games,
                neural_network_canvas,
                chart_canvas,
                best_game_canvas,
                *labels
            )

        win.center()
        win.mainloop()

Main(True)