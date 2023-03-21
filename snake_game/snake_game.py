from tkinter import Tk, Canvas, Event

from snake_game.UI import UI
from snake_game.snake import Snake
from snake_game.food import Food
from snake_game.custom_types import Coord
from snake_game.config import GAME_SIZE, GAME_GRID, ENERGY, FPS, BG_COLORS, DARK_COLOR, FONT_CONFIG, MESSAGE_COLOR

from neural_network import NeuralNetwork
from neural_network.config import INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZES, OUTPUT_LAYER_SIZE

class SnakeGame:
    def __init__(self, canvas: Canvas, is_ai: bool = False):
        self.canvas = canvas

        self.brain = NeuralNetwork(
            INPUT_LAYER_SIZE,
            HIDDEN_LAYER_SIZES,
            OUTPUT_LAYER_SIZE,
        )

        self.create_bg()

        self.energy = ENERGY

        self.snake = Snake(canvas)
        self.food = Food(self, canvas)

        self.is_paused = True

        self.create_message('Jogar Snake')

        keys = ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']

        if not is_ai:
            for key in keys:
                self.canvas.bind(key, self.key_event)
                
            self.canvas.focus_set()

    def key_event(self, event: Event):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.start()

    def start(self):
        self.is_paused = False
        self.energy = ENERGY

        self.remove_message()

        self.snake.reset()
        self.food.move_coord()

        self.move()

    def on_game_over(self, event: Event | None = None):
        self.is_paused = True

        self.create_message(f'Pontuacao: {self.snake.score}')

    def on_finish(self):
        self.is_paused = True

        self.create_message('Parabens!')

    def move(self):
        if self.is_paused:
            return

        snakeHeadCoord = self.snake.coords[-1][:]

        if (self.snake.direction == 'up'):
            snakeHeadCoord[1] -= 1
        elif (self.snake.direction == 'down'):
            snakeHeadCoord[1] += 1
        elif (self.snake.direction == 'left'):
            snakeHeadCoord[0] -= 1
        elif (self.snake.direction == 'right'):
            snakeHeadCoord[0] += 1

        self.snake.add_coord(snakeHeadCoord)

        isBodyColiding = snakeHeadCoord in self.snake.coords[:-1]
        isWallColiding = -1 in snakeHeadCoord or GAME_GRID in snakeHeadCoord

        if isBodyColiding or isWallColiding or self.energy == 0:
            return self.on_game_over()
        elif len(self.snake.coords) == GAME_GRID ** 2:
            return self.on_finish()
        elif snakeHeadCoord == self.food.coord:
            self.food.move_coord()
            self.energy = GAME_GRID ** 2
            self.snake.score += 1
        else:
            self.snake.remove_coord()
            self.energy -= 1

        self.canvas.after(int(1000 / FPS), self.move)

    def get_available_coords(self):
        availableSpots: list[Coord] = []

        for x in range(GAME_GRID):
            for y in range(GAME_GRID):
                coord = [x, y]

                if coord in self.snake.coords:
                    continue

                availableSpots.append(coord)

        return availableSpots

    def create_bg(self):
        UI.draw_bg(self.canvas, BG_COLORS[0], 'bg')

        for x in range(GAME_GRID):
            for y in range(GAME_GRID):
                if not ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                    continue

                UI.draw_pixel(self.canvas, [x, y], BG_COLORS[1], 'bg')

    def create_message(self, text: str):
        UI.draw_bg(self.canvas, DARK_COLOR, 'message')

        self.canvas.create_text(
            GAME_SIZE / 2,
            GAME_SIZE / 2,
            text=text,
            font=FONT_CONFIG,
            fill=MESSAGE_COLOR,
            tags='message'
        )

    def remove_message(self):
        self.canvas.delete('message')

    def get_wall_distance(self):
        head = self.snake.coords[-1]
        
        return [head[0] / GAME_GRID, head[1] / GAME_GRID, (GAME_GRID - head[0]) / 150, (GAME_GRID - head[1]) / 150]

    def get_food_distance(self):
        foodCoord = self.food.coord if self.food.coord is not None else [0, 0]

        return [(foodCoord[i] - self.snake.coords[-1][i]) for i in range(2)]

    def get_close_objects(self):
        snakeHeadCoord = self.snake.coords[-1]
        objects = []

        for x in range(3):
            for y in range(3):
                coord = [snakeHeadCoord[0] + x - 1, snakeHeadCoord[1] + y - 1]

                if coord == snakeHeadCoord:
                    continue

                if -1 in coord or GAME_GRID in coord or coord in self.snake.coords:
                    objects.append(-1)
                elif coord == self.food.coord:
                    objects.append(1)
                else:
                    objects.append(0)

        return objects