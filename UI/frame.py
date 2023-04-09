from typing import TYPE_CHECKING

from tkinter import Frame as BaseFrame

if TYPE_CHECKING:
    from tkinter import Misc

class Frame(BaseFrame):
    def __init__(
        self, 
        parent: 'Misc', 
        grid: list[int] | None = None, 
        padding: float | None = None
    ):
        super().__init__(parent)
        
        if grid is None or padding is None:
            self.pack(expand=1)
        else:
            self.grid(row=grid[0], column=grid[1], padx=padding, pady=padding)