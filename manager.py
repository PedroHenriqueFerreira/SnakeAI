from snake_game import SnakeGame
from utils import Utils
from tkinter import Event, StringVar
from random import randint

from my_types import Direction, DNA

from config import SPEED, STEP, FILE_SAVE_PATH
from config import RECORD_SCORE_TEXT, BEST_SCORE_TEXT, CURRENT_ALIVE_TEXT, GENERATION_TEXT

class Manager:
    def __init__(
        self, 
        snake_games: list[SnakeGame], 
        record_score_text: StringVar, 
        best_score_text: StringVar, 
        current_alive_text: StringVar, 
        generation_text: StringVar
    ):
        self.snake_games = snake_games
        
        self.record_score_text = record_score_text
        self.best_score_text = best_score_text
        self.current_alive_text = current_alive_text
        self.generation_text = generation_text
        
        self.record_score = 0
        self.best_score = 0
        self.current_alive = 0
        self.generation = 1

        for snake_game in snake_games:
            dna = snake_game.brain.get_DNA()
            
            snake_game.brain.set_DNA([Utils.get_random_value() for _ in dna])
            
            snake_game.start()
            
        self.load_best_players()
        self.main_loop()

    def update_record_score(self, value: int):
        self.record_score = value
        new_text = RECORD_SCORE_TEXT.replace('0', str(value))
        self.record_score_text.set(new_text)
        
    def update_best_score(self, value: int):
        self.best_score = value
        new_text = BEST_SCORE_TEXT.replace('0', str(value))
        self.best_score_text.set(new_text)
        
    def update_current_alive(self, value: int):
        self.current_alive = value
        new_text = CURRENT_ALIVE_TEXT.replace('0', str(value))
        self.current_alive_text.set(new_text)
    
    def update_generation(self, value: int):
        self.generation = value
        new_text = GENERATION_TEXT.replace('0', str(value))
        self.generation_text.set(new_text)

    def transform_output(self, output: list[float]) -> Direction:
        if output[0] > 0: return 'right'
        elif output[1] > 0: return 'down'
        elif output[2] > 0: return 'left'
        elif output[3] > 0: return 'up'
        
        return 'right'

    def main_loop(self):
        current_alive = 0

        for snake_game in self.snake_games:
            if snake_game.is_paused:
                continue
            
            current_alive += 1
            
            event: Event = Event()

            values = snake_game.get_food_distance() + snake_game.get_close_objects()

            snake_game.brain.input_layer.set_values(values)
            event.keysym = self.transform_output(snake_game.brain.calculate_output())
            
            snake_game.key_event(event)
            
            if (snake_game.snake.score > self.record_score):
                self.update_record_score(snake_game.snake.score)
                
            if (snake_game.snake.score > self.best_score):
                self.update_best_score(snake_game.snake.score)

        self.update_current_alive(current_alive)
        
        if current_alive == 0:
            self.update_best_score(0)
            self.update_generation(self.generation + 1)
            
            self.sort_best_players()
            self.save_best_players()
            self.generate_mutations()
        
            for snake_game in self.snake_games:
                snake_game.start()

        self.snake_games[0].canvas.after(SPEED, self.main_loop)

    def save_best_players(self):
        best_players = self.snake_games[0:STEP]
        
        data: dict[str, int | list[DNA]] = {}
        
        best_players_dna = [snake_game.brain.get_DNA() for snake_game in best_players]
        
        data['best_players_dna'] = best_players_dna
        data['record_score'] = self.record_score
        data['generation'] = self.generation
        
        with open(FILE_SAVE_PATH, 'w') as f:
            f.write(str(data))
            
    def load_best_players(self):
        try:
            with open(FILE_SAVE_PATH, 'r') as f:
                data: dict = eval(f.read())
                
                self.update_record_score(data['record_score'])
                self.update_generation(data['generation'])
                
                for i, snake_game in enumerate(self.snake_games[0:STEP]):
                    snake_game.brain.set_DNA(data['best_players_dna'][i])
                    
                self.generate_mutations()
        finally:
            return

    def sort_best_players(self):
        getScore = lambda snake_game: snake_game.snake.score
        self.snake_games.sort(key=getScore, reverse=True)

    def generate_mutations(self):
        for i, snake_game in enumerate(self.snake_games[STEP:]):
            best_game_index = i % STEP
            dna = self.snake_games[best_game_index].brain.get_DNA()
            
            snake_game.brain.set_DNA(dna)

            n_mutations = randint(0, len(dna) - 1)

            dna = dna[:]

            for _ in range(n_mutations):
                randomOperation = randint(0, 3)
                randomIndex = randint(0, len(dna) - 1)
                
                match randomOperation:
                    case 0:
                        dna[randomIndex] = Utils.get_random_value()
                    case 1:
                        dna[randomIndex] *= Utils.get_small_random_value()
                    case 2:
                        dna[randomIndex] += Utils.get_medium_random_value()
                    case _:
                        dna[randomIndex] -= Utils.get_medium_random_value()

            snake_game.brain.set_DNA(dna)