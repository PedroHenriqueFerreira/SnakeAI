from tkinter import Canvas, Event

from UI import UI

from neural_network import NeuralNetwork

from snake_game.food import Food
from snake_game.snake import Snake

from config import *

class SnakeGame:
    def __init__(self, canvas: Canvas, is_AI: bool = False):
        self.UI = UI(canvas)

        self.draw_bg()

        self.snake = Snake(self)
        self.food = Food(self)
        
        self.neural_network = NeuralNetwork(
            INPUT_LAYER_SIZE,
            HIDDEN_LAYER_SIZES,
            OUTPUT_LAYER_SIZE,
            ACTIVATION_FUNCTION
        )

        self.energy = GAME_GRID ** 2

        self.lives = LIVES

        self.best_score = 0
        self.score = 0
        
        self.is_paused = True

        self.draw_message('Jogar Snake')

        if not is_AI:
            keys = ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']

            for key in keys:
                canvas.bind(key, self.on_key_event)

            canvas.focus_set()

    def on_key_event(self, event: Event):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.play()

    def play(self):
        self.is_paused = False

        self.undraw_message()

        self.energy = GAME_GRID ** 2

        self.score = 0

        self.snake.reset()
        self.food.reset()

        self.move()

    def on_game_over(self):
        if self.score > self.best_score or self.lives == LIVES:
            self.best_score = self.score

        self.lives -= 1

        if self.lives > 0:
            return self.play()

        self.lives = LIVES

        self.is_paused = True

        self.draw_message(f'Pontuacao: {self.best_score}')

    def move(self):
        if self.is_paused:
            return

        snake_head = self.snake.coords[-1].copy()

        match(self.snake.direction):
            case 'up': snake_head[1] -= 1
            case 'down': snake_head[1] += 1
            case 'left': snake_head[0] -= 1
            case 'right': snake_head[0] += 1

        isBodyColiding = snake_head in self.snake.coords
        isWallColiding = -1 in snake_head or GAME_GRID in snake_head

        if isBodyColiding or isWallColiding or self.energy == 0:
            return self.on_game_over()

        self.snake.add_coord(snake_head)

        if snake_head == self.food.coord:
            self.score += 1

            self.food.reset()

            self.energy = GAME_GRID ** 2
        else:
            self.snake.remove_coord(0)

            self.energy -= 1

        self.UI.after(SPEED, self.move)

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
        self.UI.draw_pixel([0, 0], GAME_SIZE, GREEN_COLORS[0], 'bg')

        for i in range(2):
            for x in range(i, GAME_GRID, 2):
                for y in range(1 - i, GAME_GRID, 2):
                    self.UI.draw_pixel(
                        [x, y],
                        GAME_SIZE / GAME_GRID,
                        GREEN_COLORS[1],
                        'bg'
                    )

    def draw_message(self, text: str):
        self.UI.draw_pixel(
            [0, 0],
            GAME_SIZE,
            DARK_COLOR,
            'message'
        )

        self.UI.draw_text(
            [GAME_SIZE / 2, GAME_SIZE / 2],
            LIGHT_COLOR,
            text,
            GAME_FONT,
            'message'
        )

    def undraw_message(self):
        self.UI.clear('message')

    def get_values(self):
        snake_head = self.snake.coords[-1]
        
        food_data: list[float] = []
        
        for i in range(2):
            if self.food.coord[i] < snake_head[i]:
                food_data.append(1)
                food_data.append(0)
            elif self.food.coord[i] > snake_head[i]:
                food_data.append(0)
                food_data.append(1)
            else:
                food_data.append(0)
                food_data.append(0)
        
        up = [snake_head[0] - 1, snake_head[1]]
        right = [snake_head[0], snake_head[1] + 1]
        down = [snake_head[0] + 1, snake_head[1]]
        left = [snake_head[0], snake_head[1] - 1]
        
        snake_body = self.snake.coords[:-1]
        
        near_object_data: list[int] = []
        
        for coord in [up, right, down, left]:
            if coord in snake_body or -1 in coord or GAME_GRID in coord:
                near_object_data.append(1)
                near_object_data.append(0)
            else:
                near_object_data.append(0)
                near_object_data.append(0)
        
        return food_data + near_object_data