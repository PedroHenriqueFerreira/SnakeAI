from tkinter import Canvas, Event
from random import choice

from neural_network import NeuralNetwork

from UI import UI

from config import DARK_COLOR, GREEN_COLORS, BLUE_COLORS, RED_COLOR, GAME_GRID, INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZES, OUTPUT_LAYER_SIZE, FPS, GAME_SIZE, LIGHT_COLOR, FONT_CONFIG

from custom_types import Coord, Direction

class Snake:
    def __init__(self, canvas: Canvas):
        self.UI = UI(canvas)

        self.coords: list[Coord] = []
        self.rectangles: list = []

        self.direction: Direction = 'right'
        self.score = 0
        
        self.color_index = 0

        self.reset()

    def reset(self):
        self.UI.clear('snake')

        self.coords.clear()
        self.rectangles.clear()

        self.direction = 'right'
        self.score = 0
        
        self.color_index = 0

        for coord in self.get_initial_coord():
            self.add_coord(coord)

    def add_coord(self, coord: Coord):
        self.coords.append(coord)

        rectangle = self.UI.draw_pixel(coord, BLUE_COLORS[self.color_index], 'snake')

        self.color_index = int(not self.color_index)

        self.rectangles.append(rectangle)

    def remove_coord(self):
        self.coords.pop(0)

        self.UI.clear(self.rectangles.pop(0))

    def get_initial_coord(self) -> list[Coord]:
        x = int(GAME_GRID / 4)
        y = int(GAME_GRID / 2)

        return [[x, y], [x + 1, y], [x + 2, y]]

    def change_direction(self, direction: str):
        match direction.lower():
            case 'up' | 'w':
                if self.direction != 'down':
                    self.direction = 'up'
            case 'right' | 'd':
                if self.direction != 'left':
                    self.direction = 'right'
            case 'down' | 's':
                if self.direction != 'up':
                    self.direction = 'down'
            case 'left' | 'a':
                if self.direction != 'right':
                    self.direction = 'left'

class Food:
    def __init__(self, game, canvas: Canvas):
        self.UI = UI(canvas)
        self.game = game

        self.coord: Coord | None = None

        self.move_coord()

    def move_coord(self):
        self.UI.clear('food')

        self.coord = self.get_random_coord()

        if self.coord is None: return
        
        self.UI.draw_pixel(self.coord, RED_COLOR, 'food')

    def get_random_coord(self):
        availableSpots: list[Coord] = self.game.get_available_coords()

        if len(availableSpots) == 0: return None

        return choice(availableSpots)

class Game:
    def __init__(self, canvas: Canvas, is_ai: bool = False):
        self.UI = UI(canvas)

        self.brain = NeuralNetwork(
            INPUT_LAYER_SIZE,
            HIDDEN_LAYER_SIZES,
            OUTPUT_LAYER_SIZE,
        )

        self.create_bg()

        self.energy = GAME_GRID ** 2

        self.snake = Snake(canvas)
        self.food = Food(self, canvas)

        self.is_paused = True

        self.create_message('Jogar Snake')

        keys = ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']

        if not is_ai:
            for key in keys:
                canvas.bind(key, self.key_event)
                
            canvas.focus_set()

    def key_event(self, event: Event):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.start()

    def start(self):
        self.is_paused = False
        self.energy = GAME_GRID ** 2

        self.remove_message()

        self.snake.reset()
        self.food.move_coord()

        self.move()

    def on_game_over(self, _: Event | None = None):
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

        self.UI.canvas.after(int(1000 / FPS), self.move)

    def get_available_coords(self):
        availableSpots: list[Coord] = []

        for x in range(GAME_GRID):
            for y in range(GAME_GRID):
                coord = [float(x), float(y)]

                if coord in self.snake.coords:
                    continue

                availableSpots.append(coord)

        return availableSpots

    def create_bg(self):
        self.UI.draw_bg(GREEN_COLORS[0], 'bg')

        for i in range(2):
            for x in range(i, GAME_GRID, 2):
                for y in range(1 - i, GAME_GRID, 2):    
                    self.UI.draw_pixel([x, y], GREEN_COLORS[1], 'bg')

    def create_message(self, text: str):
        self.UI.draw_bg(DARK_COLOR, 'message')

        self.UI.draw_text([GAME_SIZE / 2, GAME_SIZE / 2], LIGHT_COLOR, text, FONT_CONFIG, 'message')

    def remove_message(self):
        self.UI.clear('message')

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