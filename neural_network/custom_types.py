from typing import Literal

LayerType = Literal['input', 'hidden', 'output']

Activation = Literal['sigmoid', 'relu', 'step']

DNA = list[float]
Coord = list[float]