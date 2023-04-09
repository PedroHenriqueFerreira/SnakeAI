from typing import TYPE_CHECKING, Literal

from config import *

if TYPE_CHECKING:
    from snake_game.snake_game import SnakeGame

class Snake:
    def __init__(self, game: 'SnakeGame'):
        self.game = game

        self.coords: list[list[float]] = []

        self.direction: Literal['up', 'right', 'down', 'left'] = 'right'

    def reset(self):
        self.game.canvas.delete('snake')

        self.coords.clear()

        self.direction = 'right'

        for coord in self.get_initial_coords():
            self.add_head(coord)

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

    def get_next_head(self):
        head = self.coords[-1].copy()
        
        match(self.direction):
            case 'up': head[1] -= 1
            case 'down': head[1] += 1
            case 'left': head[0] -= 1
            case 'right': head[0] += 1
            
        return head

    def add_head(self, coord: list[float]):
        self.coords.append(coord)

        self.game.canvas.draw_pixel(
            coord,
            GAME_SIZE / GAME_GRID,
            BLUE_COLOR,
            'snake'
        )

    def remove_tail(self):
        self.coords.pop(0)
        
        snake_elements = self.game.canvas.find_withtag('snake')
        
        self.game.canvas.delete(snake_elements[0])

    def get_initial_coords(self) -> list[list[float]]:
        x = int(GAME_GRID / 4)
        y = int(GAME_GRID / 2)

        return [[x + i, y] for i in range(3)]
    
    def get_score(self):
        return len(self.coords) - len(self.get_initial_coords())