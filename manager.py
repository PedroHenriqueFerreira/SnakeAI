from tkinter import Event, StringVar, Canvas

from game import SnakeGame
from neural_network import NeuralNetwork

from chart import Chart

from UI import UI

from config import *

class Manager:
    def __init__(
        self,
        snake_games: list[SnakeGame],
        neural_network_canvas: Canvas,
        chart_canvas: Canvas,
        best_game_canvas: Canvas,
        best_score_text: StringVar,
        current_best_score_text: StringVar,
        current_alive_text: StringVar,
        past_generations_text: StringVar,
    ):
        self.chart = Chart(chart_canvas)

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

        for snake_game in snake_games:
            snake_game.brain = NeuralNetwork(
                neural_network_canvas, 
                INPUT_LAYER_SIZE, 
                HIDDEN_LAYER_SIZES, 
                OUTPUT_LAYER_SIZE,
                ACTIVATION_FUNCTION
            )
            
            snake_game.start()
            
        self.snake_games[0].brain.draw()
        self.snake_games[0].draw_best_game()
        self.chart.draw()

        self.load_data()
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

    def transform_output(self, output: list[float]):
        if output[0] > 0:
            return 'right'
        elif output[1] > 0:
            return 'down'
        elif output[2] > 0:
            return 'left'
        elif output[3] > 0:
            return 'up'

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

            current_score = snake_game.snake.score
            best_snake_score = self.snake_games[best_index].snake.score

            if (current_score > self.best_score):
                self.update_best_score(current_score)

            if (current_score > self.current_best_score):
                self.update_current_best_score(current_score)

            if current_score > best_snake_score or self.snake_games[best_index].is_paused:
                best_index = i
        
        self.snake_games[best_index].brain.draw_update()

        self.snake_games[best_index].update_best_game()

        self.update_current_alive(current_alive)
        
        if current_alive == 0:
            self.best_score_history.append(self.current_best_score)
            self.chart.draw_update(self.best_score_history)
            
            self.update_current_best_score(0)
                
            self.update_past_generations(self.generation + 1)

            self.sort_best_score()
            self.save_data()
            self.generate_mutations()
            
            for snake_game in self.snake_games:
                snake_game.snake.score = 0
                snake_game.start()

        self.snake_games[0].UI.after(FPS, self.main_loop)

    def save_data(self):
        best_players = self.snake_games[0:BEST_PLAYERS]

        data: dict = {
            'best_players_dna': [snake_game.brain.get_DNA() for snake_game in best_players],
            'best_score': self.best_score,
            'generation': self.generation,
            'best_score_history': self.best_score_history
        }

        with open(FILE_SAVE_PATH, 'w') as f:
            f.write(str(data))

    def load_data(self):
        try:
            with open(FILE_SAVE_PATH, 'r') as f:
                data: dict = eval(f.read())

                self.update_best_score(data['best_score'])
                self.update_past_generations(data['generation'])

                self.best_score_history = data['best_score_history']
                self.chart.draw_update(self.best_score_history)

                for i, snake_game in enumerate(self.snake_games[0:BEST_PLAYERS]):
                    snake_game.brain.set_DNA(data['best_players_dna'][i])

                self.generate_mutations()
        finally:
            return

    def sort_best_score(self):
        self.snake_games.sort(
            key=lambda snake_game: snake_game.snake.score, 
            reverse=True
        )

    def generate_mutations(self):
        for i, snake_game in enumerate(self.snake_games[BEST_PLAYERS:]):
            index = i % BEST_PLAYERS
            dna = self.snake_games[index].brain.get_DNA()
            
            snake_game.brain.set_DNA(dna)
            snake_game.brain.generate_DNA_mutation()
