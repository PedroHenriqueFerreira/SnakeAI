from typing import TYPE_CHECKING, Literal

from config import *

if TYPE_CHECKING:
    from game import SnakeGame

class Snake:
    def __init__(self, game: 'SnakeGame'):
        self.game = game

        self.coords: list[list[float]] = []

        self.direction: Literal['up', 'right', 'down', 'left'] = 'right'

    def reset(self):
        self.game.canvas.delete('snake')

        self.coords.clear()

        self.direction = 'right'

        for coord in self.get_initial_coord():
            self.add_coord(coord)

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

    def add_coord(self, coord: list[float]):
        self.coords.append(coord)

        self.game.canvas.draw_pixel(
            coord,
            GAME_SIZE / GAME_GRID,
            BLUE_COLOR,
            'snake'
        )

    def remove_coord(self, idx: int):
        self.coords.pop(idx)
        
        self.game.canvas.delete(self.game.canvas.find_withtag('snake')[idx])

    def get_initial_coord(self) -> list[list[float]]:
        x = int(GAME_GRID / 4)
        y = int(GAME_GRID / 2)

        return [[x + i, y] for i in range(3)]