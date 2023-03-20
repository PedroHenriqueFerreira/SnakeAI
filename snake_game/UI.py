from tkinter import Canvas
from snake_game.custom_types import Coord

from snake_game.config import GAME_SIZE, GAME_GRID

PIXEL_SIZE = GAME_SIZE / GAME_GRID

class UI:
    @staticmethod
    def draw_bg(canvas: Canvas, fill: str, tag: str):
        return canvas.create_rectangle(
            0,
            0,
            GAME_SIZE,
            GAME_SIZE,
            fill=fill,
            width=0,
            tags=tag
        )
        
    @staticmethod
    def draw_pixel(canvas: Canvas, coord: Coord, fill: str, tag: str):
        return canvas.create_rectangle(
            coord[0] * PIXEL_SIZE,
            coord[1] * PIXEL_SIZE,
            (coord[0] + 1) * PIXEL_SIZE,
            (coord[1] + 1) * PIXEL_SIZE,
            fill=fill,
            width=0,
            tags=tag
        )