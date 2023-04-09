from typing import TYPE_CHECKING

from tkinter import Label as BaseLabel

if TYPE_CHECKING:
    from tkinter import Misc

class Label(BaseLabel):
    def __init__(self, parent: 'Misc', text: str, grid: list[int], padding: float):
        super().__init__(parent, text=text)
        
        self.grid(row=grid[0], column=grid[1], padx=padding, pady=padding)
        
        self.text = text
    
    def update_number(self, number: float):
        self.config(text=self.text.replace('0', str(number)))