from tkinter import Tk, Canvas, Frame, Label, StringVar

from snake_game import SnakeGame
from manager import Manager

from snake_game.config import GAME_SIZE, FONT_CONFIG, DARK_COLOR

from manager.config import GAMES_GRID, BEST_SCORE_TEXT, CURRENT_BEST_SCORE_TEXT, CURRENT_ALIVE_TEXT, GENERATION_TEXT, PADDING

from neural_network.config import NEURAL_NETWORK_WIDTH, NEURAL_NETWORK_HEIGHT

class Main:
    def __init__(self, is_ai: bool = False):
        win = Tk()
        win.title('Snake Game')

        root = Frame(win)
        root.pack(expand=1)
        
        if not is_ai:
            canvas = Canvas(root, width=GAME_SIZE, height=GAME_SIZE)
            canvas.pack(expand=1)

            SnakeGame(canvas)
        else:
            header = Frame(root)
            header.grid(row=0, column=0)

            best_score = StringVar(value=BEST_SCORE_TEXT)
            current_best_score = StringVar(value=CURRENT_BEST_SCORE_TEXT)
            current_alive = StringVar(value=CURRENT_ALIVE_TEXT)
            current_generation = StringVar(value=GENERATION_TEXT)

            for i, text in enumerate([best_score, current_best_score, current_alive, current_generation]):
                Label(header, textvariable=text, font=FONT_CONFIG, padx=PADDING, pady=PADDING, fg=DARK_COLOR).grid(row=0, column=i)
            
            games_grid = Frame(root)
            
            games_grid.grid(row=1, column=0)

            snake_games: list[SnakeGame] = []
            
            for x in range(GAMES_GRID[0]):
                for y in range(GAMES_GRID[1]):
                    canvas = Canvas(games_grid, width=GAME_SIZE, height=GAME_SIZE, cursor='hand1')
                    
                    canvas.grid(row=x, column=y)

                    snake_games.append(SnakeGame(canvas, True))

            neural_network_canvas = Canvas(root, width=NEURAL_NETWORK_WIDTH, height=NEURAL_NETWORK_HEIGHT)
            neural_network_canvas.grid(row=1, column=1)

            Manager(snake_games, neural_network_canvas, best_score, current_best_score, current_alive, current_generation)
            
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
