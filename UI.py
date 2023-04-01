from typing import Callable, TYPE_CHECKING
from tkinter import Canvas

from config import *

if TYPE_CHECKING:
    from snake_game import SnakeGame
    from neural_network import NeuralNetwork

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

    def draw_line(self, origin: list[float], destiny: list[float], width: int, color: str, tag: str):
        return self.canvas.create_line(
            origin[0],
            origin[1],
            destiny[0],
            destiny[1],
            width=width,
            fill=color,
            tags=tag
        )

    def draw_polygon(self, coords: list[list[float]], width: int, color: str, tag: str):
        return self.canvas.create_polygon(
            *[pos for coord in coords for pos in coord],
            fill='',
            width=width,
            outline=color,
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
    
    def draw_chart(self, values: list[float]):
        if len(self.find('line')) == 0:
            block_size = CHART_SIZE / CHART_GRID

            for i in range(CHART_GRID + 1):
                pos = i * block_size

                self.draw_line([0, pos], [CHART_SIZE, pos], LINE_WIDTH, DARK_COLOR, 'line')
                self.draw_line([pos, 0], [pos, CHART_SIZE], LINE_WIDTH, DARK_COLOR, 'line')
            
        coords: list[list[float]] = []

        if len(values) == 0 or max(values) == 0:
            return

        if len(values) > 1:
            for i, value in enumerate(values):
                x = i * (CHART_SIZE / (len(values) - 1))
                
                if i == 0:
                    x -= LINE_WIDTH
                
                if i == len(values) - 1:
                    x += LINE_WIDTH

                y = CHART_SIZE - (value / max(values)) * CHART_SIZE

                coords.append([x, y])
        else:
            coords.append([CHART_SIZE + LINE_WIDTH, 0])

        origin_coord: list[float] = [-LINE_WIDTH, CHART_SIZE + LINE_WIDTH]
        destiny_coord: list[float] = [CHART_SIZE + LINE_WIDTH, CHART_SIZE + LINE_WIDTH]
        
        all_coords = [origin_coord, *coords, destiny_coord]
        
        self.clear('chart')
        self.draw_polygon(all_coords, LINE_WIDTH, RED_COLOR, 'chart')
    
    def draw_best_game(self, snake_game: 'SnakeGame'):
        if len(self.find('bg')) == 0:
            self.draw_pixel([0, 0], BEST_GAME_SIZE, GREEN_COLORS[0], 'bg')
            
            for i in range(2):
                for x in range(i, GAME_GRID, 2):
                    for y in range(1 - i, GAME_GRID, 2):
                        self.draw_pixel(
                            [x, y],
                            BEST_GAME_SIZE / GAME_GRID,
                            GREEN_COLORS[1],
                            'bg'
                        )
        
        self.clear('food')
        self.clear('snake')
        
        if snake_game.food.coord is not None:
            self.draw_pixel(
                snake_game.food.coord,
                BEST_GAME_SIZE / GAME_GRID,
                RED_COLOR,
                'food'
            )
        
        for snake_coord in snake_game.snake.coords:
            self.draw_pixel(
                snake_coord, 
                BEST_GAME_SIZE / GAME_GRID, 
                BLUE_COLOR,
                'snake'
            )
        
    def draw_neural_network(self, neural_network: 'NeuralNetwork'):
        nn = neural_network
        
        layers = [nn.input_layer, *nn.hidden_layers, nn.output_layer]
        neurons = [neuron for layer in layers for neuron in layer.neurons]

        if all(len(self.find(i)) == 0 for i in ['neuron', 'line', 'text']):
            max_layer_len = max([len(layer.neurons) for layer in layers])
            layers_len = len(layers)
            
            width = NEURON_SIZE * layers_len
            height = NEURON_SIZE * max_layer_len
            
            x_margin = (NEURAL_NETWORK_SIZE - width) / (layers_len - 1)
            y_margin = (NEURAL_NETWORK_SIZE - height) / (max_layer_len - 1)

            prev_elements: list[int] = []
            elements: list[int] = []
            
            for layer_idx, layer in enumerate(layers):
                neurons_len = len(layer.neurons)
                
                layer_height = neurons_len * NEURON_SIZE + (neurons_len - 1) * y_margin
                
                top = (NEURAL_NETWORK_SIZE - layer_height) / 2

                for neuron_idx, neuron in enumerate(layer.neurons):
                    x = layer_idx * NEURON_SIZE + layer_idx * x_margin
                    y = top + neuron_idx * NEURON_SIZE + neuron_idx * y_margin

                    neuron_coord = [x, y]
                    text_coord = [x + NEURON_SIZE / 2, y + NEURON_SIZE / 2]
                    
                    elements.append(self.draw_circle(neuron_coord, NEURON_SIZE, DARK_COLOR, 'neuron'))
                    self.draw_text(text_coord, LIGHT_COLOR, '0.0', NEURON_FONT, 'text')

                    if neuron.wheights is None:
                        continue

                    for neuron_idx in range(len(neuron.wheights)):
                        [xi, yi, *_] = self.coords(prev_elements[neuron_idx])
                        
                        origin = [x + NEURON_SIZE / 2, y + NEURON_SIZE / 2]
                        destiny = [xi + NEURON_SIZE / 2, yi + NEURON_SIZE / 2]

                        self.draw_line(origin, destiny, LINE_WIDTH, DARK_COLOR, 'line')

                prev_elements = elements.copy()
                elements.clear()
        
        neuron_elements = self.find('neuron')
        text_elements = self.find('text')
        line_elements = self.find('line')
        
        neuron_elements_active: list[int] = []

        for i, neuron in enumerate(neurons):
            color = RED_COLOR if neuron.output > 0 else DARK_COLOR
            text = f'{neuron.output:.1f}' if neuron.output < 100 else '99.9+'

            if neuron.output > 0:
                neuron_elements_active.append(neuron_elements[i])
            
            self.element_config(neuron_elements[i], fill=color)
            self.element_config(text_elements[i], text=text)

        for line_element in line_elements:
            line_coords = self.coords(line_element)

            elements_at_line: list[int] = [
                *self.find_at_coord(line_coords[:2]),
                *self.find_at_coord(line_coords[2:])
            ]

            elements_active_at_line = set(neuron_elements_active) & set(elements_at_line)
            
            color = RED_COLOR if len(elements_active_at_line) >= 2 else DARK_COLOR

            self.element_config(line_element, fill=color)

            if len(elements_active_at_line) >= 2:
                self.move_up(line_element)

        self.move_up('neuron')
        self.move_up('text')
        
    def after(self, speed: int, func: Callable[[], None]):
        self.canvas.after(int(1000 / speed), func)
        
    def find_at_coord(self, coord: list[float]):
        return self.canvas.find_overlapping(*coord, *coord)
    
    def find(self, tag_or_id: str | int):
        return self.canvas.find_withtag(tag_or_id)
    
    def clear(self, tag_or_id: str | int):
        self.canvas.delete(tag_or_id)
        
    def coords(self, tag_or_id: str | int):
        return self.canvas.coords(tag_or_id)
    
    def element_config(self, tag_or_id: str | int, **kwargs):
        self.canvas.itemconfig(tag_or_id, **kwargs)
    
    def move_up(self, tag_or_id: str | int):
        elements = self.find(tag_or_id)
        
        for element in elements:
            self.canvas.lift(element)