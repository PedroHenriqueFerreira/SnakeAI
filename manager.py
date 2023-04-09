from snake_game import SnakeGame

from UI import Canvas, Label, Event

from config import *

class Manager:
    def __init__(
        self,
        snake_games: list[SnakeGame],
        neural_network_canvas: Canvas,
        chart_canvas: Canvas,
        best_game_canvas: Canvas,
        generation_label: Label,
        record_label: Label,
        score_label: Label,
        alive_label: Label
    ):
        self.snake_games = snake_games

        self.chart_canvas = chart_canvas
        self.neural_network_canvas = neural_network_canvas
        self.best_game_canvas = best_game_canvas
        
        self.chart_canvas.draw_chart([])

        self.record_label = record_label
        self.score_label = score_label
        self.alive_label = alive_label
        self.generation_label = generation_label
        
        self.score_history: list[int] = [0]

        for snake_game in snake_games:
            snake_game.play()

        self.load_data()
        self.main_loop()

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

            output = neural_network.get_output(snake_game.get_data())
            direction = self.transform_output(output)
            
            snake_game.on_key_event(Event(direction))

            best_game = self.snake_games[best_game_idx]
            
            if best_game.is_paused or snake_game.score > best_game.score:
                best_game_idx = i

        best_game = self.snake_games[best_game_idx]

        self.best_game_canvas.draw_best_game(best_game)
        self.neural_network_canvas.draw_neural_network(best_game.neural_network)

        score = max([max(snake_game.score, snake_game.best_score) for snake_game in self.snake_games])

        self.score_label.update_number(score)
        self.alive_label.update_number(alive)

        if alive == 0:
            self.sort_snake_games()
            
            self.score_history.append(self.snake_games[0].best_score)
            self.chart_canvas.draw_chart(self.score_history)

            self.record_label.update_number(max(self.score_history))
            self.generation_label.update_number(len(self.score_history) - 1)

            self.save_data()
            
            self.generate_mutations()

            for snake_game in self.snake_games:
                snake_game.play()

        self.best_game_canvas.after(SPEED, self.main_loop)

    def save_data(self):
        best_players = self.snake_games[0:BEST_PLAYERS_SELECT]
        best_players_DNA = [snake_game.neural_network.get_DNA() for snake_game in best_players]

        data = {
            'best_players_DNA': best_players_DNA,
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
                    
                self.score_history = data['score_history']
                
                self.chart_canvas.draw_chart(self.score_history)
                
                self.record_label.update_number(max(self.score_history))
                self.generation_label.update_number(len(self.score_history) - 1)

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
