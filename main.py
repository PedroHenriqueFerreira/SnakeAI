from tkinter import Tk, Canvas, Event
from random import randint

from constants import CANVAS_SIZE, SPEED, WINDOW_GRID
from game import Game
        
class GamesManager:
    def __init__(self, games: list[Game]):
        self.games = games
        
        for game in games:
            game.start()
        
        self.setRandomDNA()
        self.change_direction()
    
    def setRandomDNA(self):
        for game in self.games:
            game.brain.setRandomDNA()
        
    def change_direction(self):
        if all([game.is_paused for game in self.games]):
            self.generate_mutations()
            for game in self.games:
                game.is_paused = False
            
                game.start()
        
        for game in self.games:
            if game.is_paused: continue

            game.brain.input_layer.neurons[0].output = game.food_x_distance()
            game.brain.input_layer.neurons[1].output = game.food_y_distance()
            
            output = game.brain.calculateOutput()

            key = ''
            
            if output[0] > 0:
                key = 'Right'
            elif output[1] > 0:
                key = 'Left'
            elif output[2] > 0:
                key = 'Up'
            elif output[3] > 0:
                key = 'Down'
            
            event: Event = Event()
            event.keysym = key
            game.key_event(event)
        
        self.games[0].canvas.after(SPEED, self.change_direction)

    def generate_mutations(self):
        self.games.sort(key=lambda game: game.snake.score, reverse=True)
        
        print(f'Best score: {self.games[0].snake.score}')
        
        dna_length = len(self.games[0].brain.getDNA())
        
        for i, game in enumerate(self.games[2:]):
            if (i % 2) == 0:
                game.brain.setDNA(self.games[0].brain.getDNA())
            else:
                game.brain.setDNA(self.games[1].brain.getDNA())
            
            mutations = randint(0, len(self.games) - 1)
            
            dna = game.brain.getDNA()
            
            for _ in range(mutations):
                type = randint(0, 2)
                
                index = randint(0, dna_length - 1)
                
                if type == 0:
                    dna[index] = randint(-1000, 1000)
                elif type == 1:
                    dna[index] += randint(0, 500)
                else:
                    dna[index] *= randint(0, 500)
            
            game.brain.setDNA(dna)
            
class Main:
    def __init__(self):
        win = Tk()
        win.title('Snake Game')

        games = []

        for x in range(WINDOW_GRID):
            for y in range(WINDOW_GRID):
                canvas = Canvas(win, width=CANVAS_SIZE, height=CANVAS_SIZE, borderwidth=0)
                canvas.grid(row=x, column=y, padx=0, pady=0)
                
                games.append(Game(win, canvas))
        
        GamesManager(games)
        
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