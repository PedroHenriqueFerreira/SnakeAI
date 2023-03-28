from tkinter import Canvas
from typing import Callable

from config import *


class UI:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw_pixel(self, coord: list[float], size: float, color: str, tag: str):
        return self.canvas.create_rectangle(
            coord[0] * size,
            coord[1] * size,
            (coord[0] + 1) * size,
            (coord[1] + 1) * size,
            width=0,
            fill=color,
            tags=tag
        )

    def draw_text(self, coord: list[float], color: str, text: str, font: tuple[str, int], tag: str):
        return self.canvas.create_text(
            coord[0],
            coord[1],
            text=text,
            font=font,
            fill=color,
            tags=tag
        )

    def draw_line(self, origin: list[float], destiny: list[float], color: str, tag: str):
        return self.canvas.create_line(
            origin[0],
            origin[1],
            destiny[0],
            destiny[1],
            width=LINE_WIDTH,
            fill=color,
            tags=tag
        )

    def draw_circle(self, coord: list[float], size: float, color: str, tag: str):
        return self.canvas.create_oval(
            coord[0],
            coord[1],
            coord[0] + size,
            coord[1] + size,
            fill=color,
            width=0,
            tags=tag)

    def draw_polygon(self, coords: list[list[float]], color: str, tag: str):
        return self.canvas.create_polygon(
            *[pos for coord in coords for pos in coord],
            fill='',
            width=LINE_WIDTH,
            outline=color,
            tags=tag
        )
        
    def clear(self, tag_or_id: str | int):
        self.canvas.delete(tag_or_id)
        
    def coords(self, tag_or_id: str | int):
        return self.canvas.coords(tag_or_id)

    def element_config(self, tag_or_id: str | int, **kwargs):
        self.canvas.itemconfig(tag_or_id, **kwargs)

    def find(self, tag_or_id: str | int):
        return self.canvas.find_withtag(tag_or_id)
    
    def find_at_coord(self, coord: list[float]):
        return self.canvas.find_overlapping(*coord, *coord)
    
    def move_up(self, tag_or_id: str | int):
        elements = self.find(tag_or_id)
        
        for element in elements:
            self.canvas.lift(element)
            
    def after(self, fps: int, func: Callable[[], None]):
        self.canvas.after(int(1000 / fps), func)