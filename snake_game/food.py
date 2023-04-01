from typing import TYPE_CHECKING

from random import choice

from config import *

if TYPE_CHECKING:
    from game import SnakeGame

class Food:
    def __init__(self, game: 'SnakeGame'):
        self.game = game

        self.coord: list[float] | None = None

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
        availableSpots: list[list[float]] = self.game.get_available_coords()

        if len(availableSpots) == 0:
            return None

        return choice(availableSpots)