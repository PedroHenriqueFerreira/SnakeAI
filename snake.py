from tkinter import Canvas
from game_types import Pos, Direction
from constants import CANVAS_GRID, PIXEL_SIZE, SNAKE_COLORS

class Snake:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        
        self.coords: list[Pos] = []
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
        
        for pos in self.getInitialPos():
            self.add_coord(pos)

    def create_rectangle(self, pos: Pos):
        fill = SNAKE_COLORS[self.color_index]
        
        self.color_index = 1 if self.color_index == 0 else 0
        
        rectangle = self.canvas.create_rectangle(
            pos[0] * PIXEL_SIZE, 
            pos[1] * PIXEL_SIZE, 
            (pos[0] + 1) * PIXEL_SIZE, 
            (pos[1] + 1) * PIXEL_SIZE, 
            fill=fill,
            width=0,
            tags='snake'
        )
        
        self.rectangles.append(rectangle)

    def add_coord(self, pos: Pos):
        self.coords.append(pos)
        
        self.create_rectangle(pos)
    
    def remove_coord(self):
        self.coords.pop(0)
        
        rectangle = self.rectangles.pop(0)
        self.canvas.delete(rectangle)
    
    def getInitialPos(self) -> list[Pos]:
        x = int(CANVAS_GRID / 4)
        y = int(CANVAS_GRID / 2)
        
        return [[x, y], [x + 1, y], [x + 2, y]]

    def change_direction(self, direction: Direction):
        match direction:
            case 'up':
                if self.direction != 'down':
                    self.direction = 'up'
            case 'right':
                if self.direction != 'left':
                    self.direction = 'right'
            case 'down':
                if self.direction != 'up':
                    self.direction = 'down'
            case 'left':
                if self.direction != 'right':
                    self.direction = 'left'
