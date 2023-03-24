from tkinter import Canvas, Event
from random import choice

from neural_network import NeuralNetwork

from UI import UI

from config import BLACK_COLOR, GREEN_COLORS, BLUE_COLOR, RED_COLOR, GAME_GRID, INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZES, OUTPUT_LAYER_SIZE, FPS, GAME_SIZE, WHITE_COLOR, FONT_CONFIG

from custom_types import Coord, Direction


class Snake:
    def __init__(self, game: 'Game'):
        self.game = game

        self.coords: list[Coord] = []

        self.direction: Direction = 'right'

        self.score = 0
        self.energy = 0

        self.reset()

    def reset(self):
        self.game.UI.clear('snake')

        self.coords.clear()

        self.direction = 'right'

        self.score = 0
        self.energy = GAME_GRID ** 2

        for coord in self.get_initial_coord():
            self.add_coord(coord)

    def add_coord(self, coord: Coord):
        self.coords.append(coord)

        self.game.UI.draw_pixel(
            coord, 
            GAME_SIZE / GAME_GRID, 
            BLUE_COLOR, 
            'snake'
        )

    def remove_coord(self):
        self.coords.pop(0)

        self.game.UI.clear(self.game.UI.find('snake')[0])

    def get_initial_coord(self) -> list[Coord]:
        x = int(GAME_GRID / 4)
        y = int(GAME_GRID / 2)

        return [[x + i, y] for i in range(3)]

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
    def __init__(self, game: 'Game'):
        self.game = game

        self.coord: Coord | None = None

        self.reset()

    def reset(self):
        self.game.UI.clear('food')

        self.coord = self.get_random_coord()

        if self.coord is None:
            return

        self.game.UI.draw_pixel(
            self.coord,
            GAME_SIZE / GAME_GRID,
            RED_COLOR,
            'food'
        )

    def get_random_coord(self):
        availableSpots: list[Coord] = self.game.get_available_coords()

        if len(availableSpots) == 0:
            return None

        return choice(availableSpots)


class Game:
    def __init__(self, canvas: Canvas, is_ai: bool = False):
        self.UI = UI(canvas)

        self.draw_bg()

        self.snake = Snake(self)
        self.food = Food(self)

        self.is_paused = True

        self.create_message('Jogar Snake')

        self.brain = NeuralNetwork(
            INPUT_LAYER_SIZE,
            HIDDEN_LAYER_SIZES,
            OUTPUT_LAYER_SIZE,
        )

        if not is_ai:
            keys = ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']

            for key in keys:
                canvas.bind(key, self.key_event)

            canvas.focus_set()

    def key_event(self, event: Event):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.start()

    def start(self):
        self.is_paused = False

        self.remove_message()

        self.snake.reset()
        self.food.reset()

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

        snake_head = self.snake.coords[-1][:]

        match(self.snake.direction):
            case 'up': snake_head[1] -= 1
            case 'down': snake_head[1] += 1
            case 'left': snake_head[0] -= 1
            case 'right': snake_head[0] += 1

        self.snake.add_coord(snake_head)

        isBodyColiding = snake_head in self.snake.coords[:-1]
        isWallColiding = -1 in snake_head or GAME_GRID in snake_head

        if isBodyColiding or isWallColiding or self.snake.energy == 0:
            return self.on_game_over()
        elif len(self.snake.coords) == GAME_GRID ** 2:
            return self.on_finish()

        if snake_head == self.food.coord:
            self.food.reset()

            self.snake.score += 1
            self.snake.energy = GAME_GRID ** 2
        else:
            self.snake.remove_coord()
            self.snake.energy -= 1

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

    def create_message(self, text: str):
        self.UI.draw_pixel(
            [0, 0],
            GAME_SIZE,
            BLACK_COLOR,
            'message'
        )

        self.UI.draw_text(
            [GAME_SIZE / 2, GAME_SIZE / 2],
            WHITE_COLOR,
            text,
            FONT_CONFIG,
            'message'
        )

    def remove_message(self):
        self.UI.clear('message')

    def get_food_distance(self):
        snake_head = self.snake.coords[-1]
        
        if self.food.coord is None:
            return [0.0, 0.0]

        return [
            (self.food.coord[i] - snake_head[i]) / GAME_GRID 
            for i in range(2)
        ]

    def get_close_objects(self):
        snake_head = self.snake.coords[-1]
        objects: list[float] = []

        for x in range(-1, 2):
            for y in range(-1, 2):
                coord = [snake_head[0] + x, snake_head[1] + y]

                if coord == snake_head:
                    continue

                if -1 in coord or GAME_GRID in coord or coord in self.snake.coords:
                    objects.append(-1.0)
                elif coord == self.food.coord:
                    objects.append(1.0)
                else:
                    objects.append(0.0)

        return objects
