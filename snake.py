from tkinter import Canvas
from utils import Utils
from my_types import Coord, Direction
from config import CANVAS_GRID_SIZE, SNAKE_COLORS


class Snake:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

        self.coords: list[Coord] = []
        self.rectangles: list = []

        self.direction: Direction = 'right'
        self.score = 0
        self.color_index = 0

        self.reset()

    def reset(self):
        self.canvas.delete('snake')

        self.coords.clear()
        self.rectangles.clear()

        self.direction = 'right'
        self.score = 0
        self.color_index = 0

        for coord in self.get_initial_coord():
            self.add_coord(coord)

    def add_coord(self, coord: Coord):
        self.coords.append(coord)

        rectangle = Utils.create_rectangle(
            self.canvas,
            coord,
            SNAKE_COLORS[self.color_index],
            'snake'
        )

        self.color_index = 1 if self.color_index == 0 else 0

        self.rectangles.append(rectangle)

    def remove_coord(self):
        self.coords.pop(0)

        self.canvas.delete(self.rectangles.pop(0))

    def get_initial_coord(self) -> list[Coord]:
        x = int(CANVAS_GRID_SIZE / 4)
        y = int(CANVAS_GRID_SIZE / 2)

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
