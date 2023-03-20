from random import choice
from tkinter import Canvas
from snake_game.UI import UI

from snake_game.custom_types import Coord
from snake_game.config import FOOD_COLOR

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
            UI.draw_pixel(self.canvas, self.coord, FOOD_COLOR, 'food')

    def get_random_coord(self):
        availableSpots: list[Coord] = self.game.get_available_coords()

        if len(availableSpots) == 0:
            return None

        return choice(availableSpots)
