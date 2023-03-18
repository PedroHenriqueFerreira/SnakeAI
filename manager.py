from snake_game import SnakeGame
from utils import Utils
from tkinter import Event

from random import randint

from config import SPEED, STEP, FILE_SAVE_PATH
from my_types import Direction

class Manager:
    def __init__(self, snake_games: list[SnakeGame]):
        self.snake_games = snake_games

        for snake_game in snake_games:
            dna = snake_game.brain.get_DNA()
            
            snake_game.brain.set_DNA([Utils.get_random_value() for _ in dna])
            
            snake_game.start()
            
        self.load_best_players()
        self.main_loop()

    def transform_output(self, output: list[float]) -> Direction:
        if output[0] > 0: return 'right'
        elif output[1] > 0: return 'down'
        elif output[2] > 0: return 'left'
        elif output[3] > 0: return 'up'
        
        return 'right'

    def main_loop(self):
        is_all_paused = True

        for snake_game in self.snake_games:
            if snake_game.is_paused:
                continue
            
            is_all_paused = False
            
            event: Event = Event()

            snake_game.brain.input_layer.set_values(snake_game.get_food_distance())
            event.keysym = self.transform_output(snake_game.brain.calculate_output())
            
            snake_game.key_event(event)

        if is_all_paused:
            self.sort_snake_games()
            self.generate_mutations()
        
            for snake_game in self.snake_games:
                snake_game.start()

        self.snake_games[0].canvas.after(SPEED, self.main_loop)

    def save_best_players(self):
        best_players = self.snake_games[0:STEP]
        
        best_players_dna = [snake_game.brain.get_DNA() for snake_game in best_players]
        
        with open(FILE_SAVE_PATH, 'w') as f:
            f.write(str(best_players_dna))
            
    def load_best_players(self):
        try:
            with open(FILE_SAVE_PATH, 'r') as f:
                best_players_dna = eval(f.read())
                
                for i, snake_game in enumerate(self.snake_games[0:STEP]):
                    snake_game.brain.set_DNA(best_players_dna[i])
                    
                self.generate_mutations()
        finally:
            return

    def sort_snake_games(self):
        self.snake_games.sort(key=lambda game: game.snake.score, reverse=True)

    def generate_mutations(self):
        print(f'Best Score: {self.snake_games[0].snake.score}')
        
        self.save_best_players()
        
        for i, snake_game in enumerate(self.snake_games[STEP:]):
            best_game_index = i % STEP
            dna = self.snake_games[best_game_index].brain.get_DNA()
            
            snake_game.brain.set_DNA(dna)

            n_mutations = randint(0, len(dna) - 1)

            dna = dna[:]

            for _ in range(n_mutations):
                type = randint(0, 3)

                index = randint(0, len(dna) - 1)

                if type == 0:
                    dna[index] = Utils.get_random_value()
                elif type == 1:
                    dna[index] += Utils.get_medium_random_value()
                elif type == 2:
                    dna[index] -= Utils.get_medium_random_value()
                else: 
                    dna[index] *= Utils.get_small_random_value()

            snake_game.brain.set_DNA(dna)
