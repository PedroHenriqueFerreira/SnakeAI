from tkinter import Canvas
from utils import Utils
from my_types import Coord
from config import FOOD_COLOR
from random import choice

class Food:
    def __init__(self, game, canvas: Canvas):
        self.canvas = canvas
        self.game = game

        self.coord: Coord | None = None

        self.move_coord()

    def move_coord(self):
        self.canvas.delete('food')

        self.coord = self.get_random_coord()

        if self.coord is not None:
            Utils.create_rectangle(self.canvas, self.coord, FOOD_COLOR, 'food')

    def get_random_coord(self):
        availableSpots: list[Coord] = self.game.get_available_coords()

        if len(availableSpots) == 0:
            return None

        return choice(availableSpots)
