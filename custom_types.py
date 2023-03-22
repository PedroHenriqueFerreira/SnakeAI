from typing import Literal, Callable

Coord = list[float]
Direction = Literal['up', 'right', 'down', 'left']

ActivationFunction = Callable[[float], float]
DNA = list[float]