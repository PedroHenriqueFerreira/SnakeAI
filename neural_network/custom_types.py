from typing import Literal

LayerType = Literal['input', 'hidden', 'output']

Activation = Literal['sigmoid', 'relu']

DNA = list[float]
Coord = list[float]