from tkinter import Tk, Canvas, Event
from neural_network import NeuralNetwork
from snake import Snake
from food import Food
from utils import Utils

from my_types import Coord

from config import CANVAS_GRID_SIZE, CANVAS_SIZE, SPEED, FONT_CONFIG
from config import INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZES, OUTPUT_LAYER_SIZE
from config import BG_COLORS, DARK_COLOR, MESSAGE_COLOR

class SnakeGame:
    def __init__(self, win: Tk, canvas: Canvas, is_ai: bool = False):
        self.canvas = canvas

        self.brain = NeuralNetwork(
            INPUT_LAYER_SIZE,
            HIDDEN_LAYER_SIZES,
            OUTPUT_LAYER_SIZE
        )

        self.create_bg()

        self.energy = 0

        self.snake = Snake(canvas)
        self.food = Food(self, canvas)

        self.is_paused = True

        self.create_message('Jogar Snake')

        keys = ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']
        
        if not is_ai:
            for key in keys: win.bind(key, self.key_event) 

    def key_event(self, event: Event):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.start()

    def start(self):
        self.is_paused = False
        self.energy = CANVAS_GRID_SIZE ** 2

        self.remove_message()

        self.snake.reset()
        self.food.move_coord()

        self.move()

    def on_game_over(self):
        self.is_paused = True

        self.create_message(f'Pontuacao: {self.snake.score}')

    def on_finish(self):
        self.is_paused = True

        self.create_message('Parabens!')

    def move(self):
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
        isWallColiding = -1 in snakeHeadCoord or CANVAS_GRID_SIZE in snakeHeadCoord

        if isBodyColiding or isWallColiding:
            return self.on_game_over()
        elif len(self.snake.coords) == CANVAS_GRID_SIZE ** 2:
            return self.on_finish()
        elif snakeHeadCoord == self.food.coord:
            self.food.move_coord()
            self.energy = CANVAS_GRID_SIZE ** 2
            self.snake.score += 1
        else:
            self.snake.remove_coord()
            self.energy -= 1
            
            if (self.energy == 0):
                return self.on_game_over()
        
        self.canvas.after(SPEED, self.move)

    def get_available_coords(self):
        availableSpots: list[Coord] = []

        for x in range(CANVAS_GRID_SIZE):
            for y in range(CANVAS_GRID_SIZE):
                coord = [x, y]

                if coord in self.snake.coords:
                    continue

                availableSpots.append(coord)

        return availableSpots

    def create_bg(self):
        Utils.create_full_rectangle(self.canvas, BG_COLORS[0], 'bg')

        for x in range(CANVAS_GRID_SIZE):
            for y in range(CANVAS_GRID_SIZE):
                if not ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                    continue

                Utils.create_rectangle(self.canvas, [x, y], BG_COLORS[1], 'bg')

    def create_message(self, text: str):
        Utils.create_full_rectangle(self.canvas, DARK_COLOR, 'message')

        self.canvas.create_text(
            CANVAS_SIZE / 2,
            CANVAS_SIZE / 2,
            text=text,
            font=FONT_CONFIG,
            fill=MESSAGE_COLOR,
            tags='message'
        )

    def remove_message(self):
        self.canvas.delete('message')

    def get_food_distance(self):
        foodCoord = self.food.coord if self.food.coord is not None else [0, 0]
        
        return [foodCoord[i] - self.snake.coords[-1][i] for i in range(2)]

    def get_close_objects(self):
        snakeHeadCoord = self.snake.coords[-1]
        objects = []
        
        for x in range(3):
            for y in range(3):
                coord = [snakeHeadCoord[0] + x - 1, snakeHeadCoord[1] + y - 1]

                if coord == snakeHeadCoord:
                    continue
                
                if -1 in coord or CANVAS_GRID_SIZE in coord:
                    objects.append(-1)
                elif coord in self.snake.coords:
                    objects.append(1)
                elif coord == self.food.coord:
                    objects.append(2)
                else:
                    objects.append(0)
        
        return objects