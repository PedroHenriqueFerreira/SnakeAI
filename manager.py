from tkinter import Event, StringVar, Canvas

from snake_game import SnakeGame

from UI import UI

from config import *


class Manager:
    def __init__(
        self,
        snake_games: list[SnakeGame],
        neural_network_canvas: Canvas,
        chart_canvas: Canvas,
        best_game_canvas: Canvas,
        record_text: StringVar,
        score_text: StringVar,
        alive_text: StringVar,
        generation_text: StringVar,
    ):
        self.snake_games = snake_games

        self.chart_UI = UI(chart_canvas)
        self.chart_UI.draw_chart([])
        
        self.neural_network_UI = UI(neural_network_canvas)
        self.best_game_UI = UI(best_game_canvas)

        self.record_text = record_text
        self.score_text = score_text
        self.alive_text = alive_text
        self.generation_text = generation_text

        self.score = 0
        self.record = 0
        self.generation = 0

        self.score_history: list[int] = []

        for snake_game in snake_games:
            snake_game.play()

        self.load_data()
        self.main_loop()

    def update_generation(self, value: int):
        self.generation = value
        self.generation_text.set(GENERATION_TEXT.replace('0', str(value)))

    def update_score(self, value: int):
        self.score = value
        self.score_text.set(SCORE_TEXT.replace('0', str(value)))

    def update_record(self, value: int):
        self.record = value
        self.record_text.set(RECORD_TEXT.replace('0', str(value)))

    def update_alive(self, value: int):
        self.alive_text.set(ALIVE_TEXT.replace('0', str(value)))

    def transform_output(self, output: list[float]):
        if output[0] > 0:
            return 'up'
        elif output[1] > 0:
            return 'right'
        elif output[2] > 0:
            return 'down'
        elif output[3] > 0:
            return 'left'

        return 'right'

    def main_loop(self):
        alive = 0
        best_game_idx = 0

        for i, snake_game in enumerate(self.snake_games):
            if snake_game.is_paused:
                continue

            alive += 1
            
            neural_network = snake_game.neural_network
            
            neural_network.input_layer.set_values(snake_game.get_values())
            output = self.transform_output(neural_network.calculate_output())
            
            event: Event = Event()
            event.keysym = output
            snake_game.on_key_event(event)

            if (snake_game.score > self.record):
                self.record = snake_game.score

            if (snake_game.score > self.score):
                self.score = snake_game.score

            if self.snake_games[best_game_idx].is_paused:
                best_game_idx = i

            if snake_game.score > self.snake_games[best_game_idx].score:
                best_game_idx = i

        best_game = self.snake_games[best_game_idx]

        self.best_game_UI.draw_best_game(best_game)
        self.neural_network_UI.draw_neural_network(best_game.neural_network)

        self.update_record(self.record)
        self.update_score(self.score)
        self.update_alive(alive)

        if alive == 0:
            self.score_history.append(self.score)
            self.chart_UI.draw_chart(self.score_history)

            self.update_generation(self.generation + 1)
            self.update_score(0)

            self.sort_snake_games()
            self.save_data()
            
            self.generate_mutations()

            for snake_game in self.snake_games:
                snake_game.play()

        self.snake_games[0].UI.after(SPEED, self.main_loop)

    def save_data(self):
        best_players = self.snake_games[0:BEST_PLAYERS_SELECT]
        best_players_DNA = [snake_game.neural_network.get_DNA() for snake_game in best_players]

        data = {
            'best_players_DNA': best_players_DNA,
            'record': self.record,
            'generation': self.generation,
            'score_history': self.score_history
        }

        with open(DATA_FILE, 'w') as file:
            file.write(str(data))

    def load_data(self):
        try:
            with open(DATA_FILE, 'r') as file:
                data = eval(file.read())

                for i, DNA in enumerate(data['best_players_DNA']):
                    self.snake_games[i].neural_network.set_DNA(DNA)
                    
                self.update_record(data['record'])
                self.update_generation(data['generation'])

                self.score_history = data['score_history']
                self.chart_UI.draw_chart(self.score_history)

                self.generate_mutations()
        finally:
            return

    def sort_snake_games(self):
        self.snake_games.sort(
            key=lambda snake_game: snake_game.best_score,
            reverse=True
        )

    def generate_mutations(self):
        for i, snake_game in enumerate(self.snake_games[BEST_PLAYERS_SELECT:]):
            index = i % BEST_PLAYERS_SELECT
            DNA = self.snake_games[index].neural_network.get_DNA()

            snake_game.neural_network.set_DNA(DNA)
            snake_game.neural_network.generate_DNA_mutation()
