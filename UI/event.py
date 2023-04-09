from tkinter import Event as BaseEvent

class Event(BaseEvent):
    def __init__(self, key: str):
        super().__init__()
        
        self.keysym = key