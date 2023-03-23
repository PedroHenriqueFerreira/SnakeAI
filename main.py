from tkinter import Tk, Canvas, Frame, Label, StringVar

from game import Game
from manager import Manager

from utils import Utils

from config import GAMES_HORIZONTAL_GRID, GAMES_VERTICAL_GRID, BEST_SCORE_TEXT, CURRENT_BEST_SCORE_TEXT, CURRENT_ALIVE_TEXT, PAST_GENERATIONS_TEXT, PADDING, GAME_SIZE, FONT_CONFIG, DARK_COLOR, CHART_SIZE

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
            header = Frame(root)
            header.grid(row=0, column=0)

            best_score = StringVar(value=BEST_SCORE_TEXT)
            current_best_score = StringVar(value=CURRENT_BEST_SCORE_TEXT)
            current_alive = StringVar(value=CURRENT_ALIVE_TEXT)
            past_generations = StringVar(value=PAST_GENERATIONS_TEXT)

            for i, text in enumerate([best_score, current_best_score, current_alive, past_generations]):
                label = Label(header, textvariable=text, font=FONT_CONFIG, fg=DARK_COLOR)
                label.grid(row=0, column=i, padx=PADDING)
            
            games = Frame(root)
            games.grid(row=1, column=0)

            snake_games: list[Game] = []
            
            for x in range(GAMES_VERTICAL_GRID):
                for y in range(GAMES_HORIZONTAL_GRID):
                    canvas = Canvas(games, width=GAME_SIZE, height=GAME_SIZE)
                    canvas.grid(row=x, column=y)

                    snake_games.append(Game(canvas, True))

            sidebar = Frame(root)
            sidebar.grid(row=1, column=1, padx=PADDING)
    
            neural_network_canvas = Canvas(
                sidebar, 
                width=Utils.get_neural_network_width(), 
                height=Utils.get_neural_network_height()
            )
            neural_network_canvas.grid(row=0, column=0, pady=PADDING)   
            
            chart_canvas = Canvas(sidebar, width=CHART_SIZE, height=CHART_SIZE)
            chart_canvas.grid(row=1, column=0, pady=PADDING)

            Manager(snake_games, neural_network_canvas, chart_canvas, best_score, current_best_score, current_alive, past_generations)
            
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
