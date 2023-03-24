from game import Game
from tkinter import Event, StringVar, Canvas

from config import FPS

from custom_types import Direction
from UI import UI

from config import TOP_PLAYERS, FILE_SAVE_PATH, BEST_SCORE_TEXT, CURRENT_BEST_SCORE_TEXT, CURRENT_ALIVE_TEXT, PAST_GENERATIONS_TEXT

class Manager:
    def __init__(
        self, 
        snake_games: list[Game], 
        neural_network_canvas: Canvas,
        chart_canvas: Canvas,
        best_player_canvas: Canvas,
        best_score_text: StringVar, 
        current_best_score_text: StringVar, 
        current_alive_text: StringVar, 
        past_generations_text: StringVar,
    ):  
        self.neural_network_UI = UI(neural_network_canvas)
        self.chart_UI = UI(chart_canvas)
        self.best_player_UI = UI(best_player_canvas)
        
        self.snake_games = snake_games
        
        self.best_score_text = best_score_text
        self.current_best_score_text = current_best_score_text
        self.current_alive_text = current_alive_text
        self.past_generations_text = past_generations_text
        
        self.best_score = 0
        self.current_best_score = 0
        self.current_alive = 0
        self.generation = 0
        
        self.best_score_history: list[int] = []

        self.neural_network_UI.draw_neural_network(self.snake_games[0].brain)
        self.chart_UI.draw_chart()
        self.best_player_UI.draw_best_game(self.snake_games[0])
        
        for snake_game in snake_games: snake_game.start()
        
        self.load_best_players()
        self.main_loop()

    def update_best_score(self, value: int):
        self.best_score = value
        new_text = BEST_SCORE_TEXT.replace('0', str(value))
        self.best_score_text.set(new_text)
        
    def update_current_best_score(self, value: int):
        self.current_best_score = value
        new_text = CURRENT_BEST_SCORE_TEXT.replace('0', str(value))
        self.current_best_score_text.set(new_text)
    
    def update_current_alive(self, value: int):
        self.current_alive = value
        new_text = CURRENT_ALIVE_TEXT.replace('0', str(value))
        self.current_alive_text.set(new_text)
    
    def update_past_generations(self, value: int):
        self.generation = value
        new_text = PAST_GENERATIONS_TEXT.replace('0', str(value))
        self.past_generations_text.set(new_text)

    def transform_output(self, output: list[float]) -> Direction:
        if output[0] > 0: return 'right'
        elif output[1] > 0: return 'down'
        elif output[2] > 0: return 'left'
        elif output[3] > 0: return 'up'
        
        return 'right'

    def main_loop(self):
        current_alive = 0
        best_index = 0

        for i, snake_game in enumerate(self.snake_games):
            if snake_game.is_paused:
                continue
            
            current_alive += 1
            
            event: Event = Event()

            values = snake_game.get_food_distance() + snake_game.get_close_objects()

            snake_game.brain.input_layer.set_output(values)
            event.keysym = self.transform_output(snake_game.brain.calculate_output())
            
            snake_game.key_event(event)
            
            if (snake_game.snake.score > self.best_score):
                self.update_best_score(snake_game.snake.score)
                
            if (snake_game.snake.score > self.current_best_score):
                self.update_current_best_score(snake_game.snake.score)
                
            if snake_game.snake.score > self.snake_games[best_index].snake.score or self.snake_games[best_index].is_paused:
                best_index = i

        self.neural_network_UI.update_neural_network(self.snake_games[best_index].brain)
        
        self.update_current_alive(current_alive)
        
        if current_alive == 0:
            self.best_score_history.append(self.current_best_score)
            self.chart_UI.update_chart(self.best_score_history)
            
            self.update_current_best_score(0)
            self.update_past_generations(self.generation + 1)
            
            self.sort_best_players()
            self.save_best_players()
            self.generate_mutations()
        
            for snake_game in self.snake_games:
                snake_game.start()

        self.snake_games[0].UI.canvas.after(int(1000 / FPS), self.main_loop)

    def save_best_players(self):
        best_players = self.snake_games[0:TOP_PLAYERS]
        
        data: dict = {}
        
        best_players_dna = [snake_game.brain.get_DNA() for snake_game in best_players]
        
        data['best_players_dna'] = best_players_dna
        data['best_score'] = self.best_score
        data['generation'] = self.generation
        data['best_score_history'] = self.best_score_history
        
        with open(FILE_SAVE_PATH, 'w') as f:
            f.write(str(data))
            
    def load_best_players(self):
        try:
            with open(FILE_SAVE_PATH, 'r') as f:
                data: dict = eval(f.read())
                
                self.update_best_score(data['best_score'])
                self.update_past_generations(data['generation'])
                
                self.best_score_history = data['best_score_history']
                self.chart_UI.update_chart(self.best_score_history)
                
                for i, snake_game in enumerate(self.snake_games[0:TOP_PLAYERS]):
                    snake_game.brain.set_DNA(data['best_players_dna'][i])
                    
                self.generate_mutations()
        finally:
            return

    def sort_best_players(self):
        getScore = lambda snake_game: snake_game.snake.score
        self.snake_games.sort(key=getScore, reverse=True)

    def generate_mutations(self):
        for i, snake_game in enumerate(self.snake_games[TOP_PLAYERS:]):
            index = i % TOP_PLAYERS
            dna = self.snake_games[index].brain.get_DNA()
            
            snake_game.brain.generate_DNA_mutation(dna)