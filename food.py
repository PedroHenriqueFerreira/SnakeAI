from tkinter import Canvas
from game_types import Pos
from constants import PIXEL_SIZE, FOOD_COLOR
from random import choice

class Food:
    def __init__(self, game, canvas: Canvas):
        self.canvas = canvas
        self.game = game
        
        self.coord = self.move_coord()
    
    def move_coord(self):
        self.canvas.delete('food')
        
        coord = self.getRandomPos()
        
        if coord is not None:
            self.create_rectangle(coord)
        
        return coord
    
    def create_rectangle(self, pos: Pos):
        self.canvas.create_rectangle(
            pos[0] * PIXEL_SIZE, 
            pos[1] * PIXEL_SIZE, 
            (pos[0] + 1) * PIXEL_SIZE, 
            (pos[1] + 1) * PIXEL_SIZE, 
            fill=FOOD_COLOR,
            width=0,
            tags='food'
        )        
    
    def getRandomPos(self):
        availableSpots: list[Pos] = self.game.getAvailableSpots()
        
        if len(availableSpots) == 0:
            return None
        
        return choice(availableSpots)
