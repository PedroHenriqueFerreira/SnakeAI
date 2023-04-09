from tkinter import Tk as BaseTk

class Tk(BaseTk):
    def __init__(self, title: str, bg: str, fg: str, font: tuple[str, int]):
        super().__init__()
        
        self.title(title)
        self.config(bg=bg)
        
        self.option_add('*background', bg)
        self.option_add('*foreground', fg)
        self.option_add('*font', font)
    
    def center(self):
        self.update()

        width = self.winfo_width()
        height = self.winfo_height()

        x = int((self.winfo_screenwidth() - width) / 2)
        y = int((self.winfo_screenheight() - height) / 2)

        self.geometry(f'{width}x{height}+{x}+{y}')