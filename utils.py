from tkinter import Canvas
from random import randint

from my_types import Coord
from config import PIXEL_SIZE, CANVAS_SIZE

class Utils:
    @staticmethod
    def create_rectangle(canvas: Canvas, coord: Coord, fill: str, tag: str):
        return canvas.create_rectangle(
            coord[0] * PIXEL_SIZE,
            coord[1] * PIXEL_SIZE,
            (coord[0] + 1) * PIXEL_SIZE,
            (coord[1] + 1) * PIXEL_SIZE,
            fill=fill,
            width=0,
            tags=tag
        )

    @staticmethod
    def create_full_rectangle(canvas: Canvas, fill: str, tag: str):
        return canvas.create_rectangle(
            0,
            0,
            CANVAS_SIZE,
            CANVAS_SIZE,
            fill=fill,
            width=0,
            tags=tag
        )

    @staticmethod
    def get_random_value():
        return (randint(0, 20000) / 10.0) - 1000.0
    
    @staticmethod
    def get_medium_random_value():
        return Utils.get_random_value() / 100.0
    
    @staticmethod
    def get_small_random_value():
        return (randint(0, 10000) / 10000.0) + 0.5
    