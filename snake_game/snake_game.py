from typing import TYPE_CHECKING

from neural_network import NeuralNetwork

from snake_game.food import Food
from snake_game.snake import Snake

from config import *

if TYPE_CHECKING:
    from tkinter import Event
    from UI import Canvas

class SnakeGame:
    def __init__(self, canvas: 'Canvas', is_AI: bool = False):
        self.canvas = canvas

        self.draw_bg()

        self.snake = Snake(self)
        self.food = Food(self)
        
        self.neural_network = NeuralNetwork(
            INPUT_LAYER_SIZE,
            HIDDEN_LAYER_SIZES,
            OUTPUT_LAYER_SIZE,
            ACTIVATION_FUNCTION
        )

        self.energy = 0
        self.lives = 0
        
        self.best_score = 0
        
        self.is_paused = True

        self.draw_message('Jogar Snake')

        if not is_AI:
            canvas.bind('<Key>', self.on_key_event)
            canvas.focus_set()

    def on_key_event(self, event: 'Event'):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.play()

    def play(self):
        if self.lives == 0 or self.lives == LIVES:
            self.lives = LIVES
            self.best_score = 0
        
        self.energy = GAME_GRID ** 2
        
        self.is_paused = False

        self.undraw_message()

        self.snake.reset()
        self.food.reset()
            
        self.move()

    def on_game_over(self):
        self.lives -= 1

        if self.lives > 0:
            return self.play()

        self.is_paused = True

        self.draw_message(f'Pontuacao: {self.best_score}')

    def move(self):
        if self.is_paused:
            return

        next_head = self.snake.get_next_head()

        isBodyColiding = next_head in self.snake.coords
        isWallColiding = -1 in next_head or GAME_GRID in next_head

        if isBodyColiding or isWallColiding or self.energy == 0:
            return self.on_game_over()

        self.snake.add_head(next_head)

        if next_head == self.food.coord:
            self.food.reset()
            self.energy = GAME_GRID ** 2
        else:
            self.snake.remove_tail()
            self.energy -= 1

        current_score = self.snake.get_score()

        if current_score > self.best_score:
            self.best_score = current_score

        self.canvas.after(DELAY, self.move)

    def get_available_coords(self):
        availableSpots: list[list[float]] = []

        for x in range(GAME_GRID):
            for y in range(GAME_GRID):
                coord: list[float] = [x, y]

                if coord in self.snake.coords:
                    continue

                availableSpots.append(coord)

        return availableSpots

    def draw_bg(self):
        self.canvas.draw_pixel([0, 0], GAME_SIZE, GREEN_COLORS[0], 'bg')

        for i in range(2):
            for x in range(i, GAME_GRID, 2):
                for y in range(1 - i, GAME_GRID, 2):
                    self.canvas.draw_pixel(
                        [x, y],
                        GAME_SIZE / GAME_GRID,
                        GREEN_COLORS[1],
                        'bg'
                    )

    def draw_message(self, text: str):
        self.canvas.draw_pixel(
            [0, 0],
            GAME_SIZE,
            DARK_COLOR,
            'message'
        )

        self.canvas.draw_text(
            [GAME_SIZE / 2, GAME_SIZE / 2],
            LIGHT_COLOR,
            text,
            GAME_FONT,
            'message'
        )

    def undraw_message(self):
        self.canvas.delete('message')

    def get_data(self):
        *snake_body, snake_head = self.snake.coords
        
        food_data: list[int] = []
        near_object_data: list[int] = []
        
        for i in range(2):
            if self.food.coord[i] < snake_head[i]:
                food_data.append(1)
            elif self.food.coord[i] > snake_head[i]:
                food_data.append(-1)
            else:
                food_data.append(0)

        up = [snake_head[0] - 1, snake_head[1]]
        right = [snake_head[0], snake_head[1] + 1]
        down = [snake_head[0] + 1, snake_head[1]]
        left = [snake_head[0], snake_head[1] - 1]
        
        for coord in [up, right, down, left]:
            if coord in snake_body or -1 in coord or GAME_GRID in coord:
                near_object_data.append(1)
            else:
                near_object_data.append(0)
        
        return food_data + near_object_data