from typing import TYPE_CHECKING

from tkinter import Canvas as BaseCanvas

from config import *

if TYPE_CHECKING:
    from tkinter import Misc
    
    from snake_game import SnakeGame
    from neural_network import NeuralNetwork

class Canvas(BaseCanvas):
    def __init__(self, parent: 'Misc', size: int, grid: list[int], padding: float):
        super().__init__(parent, width=size, height=size, highlightthickness=0)
        
        self.grid(row=grid[0], column=grid[1], padx=padding, pady=padding)
    
    def get_size(self):
        return self.winfo_reqwidth()
    
    def draw_pixel(self, coord: list[float], size: float, color: str, tag: str):
        return self.create_rectangle(
            *[pos * size for pos in coord],
            *[(pos + 1) * size for pos in coord],
            width=0,
            fill=color,
            tags=tag
        )

    def draw_text(self, coord: list[float], color: str, text: str, font: tuple[str, int], tag: str):
        return self.create_text(
            *coord,
            text=text,
            font=font,
            fill=color,
            tags=tag
        )

    def draw_line(self, origin: list[float], destiny: list[float], width: int, color: str, tag: str):
        return self.create_line(
            *origin,
            *destiny,
            width=width,
            fill=color,
            tags=tag
        )

    def draw_polygon(self, coords: list[list[float]], width: int, color: str, tag: str):
        return self.create_polygon(
            *[pos for coord in coords for pos in coord],
            fill='',
            width=width,
            outline=color,
            tags=tag
        )

    def draw_circle(self, coord: list[float], size: float, color: str, tag: str):
        return self.create_oval(
            *coord,
            *[pos + size for pos in coord],
            fill=color,
            width=0,
            tags=tag)

    def draw_chart(self, values: list[float]):
        size = self.get_size()
        
        if len(self.find_withtag('line')) == 0:
            block_size = size / CHART_GRID

            for i in range(CHART_GRID + 1):
                pos = i * block_size

                self.draw_line([0, pos], [size, pos], LINE_WIDTH, DARK_COLOR, 'line')
                self.draw_line([pos, 0], [pos, size], LINE_WIDTH, DARK_COLOR, 'line')

        if len(values) == 0 or max(values) == 0:
            return
        
        coords: list[list[float]] = []
        
        coords.append([-LINE_WIDTH, size + LINE_WIDTH])
    
        if len(values) > 1:
            for i, value in enumerate(values):
                x = i * (size / (len(values) - 1))
                y = size - (value / max(values)) * size

                if x == 0:
                    coords.append([x - LINE_WIDTH, y])
                    
                coords.append([x, y])

                if x == size:
                    coords.append([x + LINE_WIDTH, y])
        else:
            coords.append([size, 0])

        coords.append([size + LINE_WIDTH, size + LINE_WIDTH])

        self.delete('chart')
        self.draw_polygon(coords, LINE_WIDTH, RED_COLOR, 'chart')
        
    def draw_best_game(self, snake_game: 'SnakeGame'):
        size = self.get_size()
        
        if len(self.find_withtag('bg')) == 0:
            self.draw_pixel([0, 0], size, GREEN_COLORS[0], 'bg')
            
            for i in range(2):
                for x in range(i, GAME_GRID, 2):
                    for y in range(1 - i, GAME_GRID, 2):
                        self.draw_pixel(
                            [x, y],
                            size / GAME_GRID,
                            GREEN_COLORS[1],
                            'bg'
                        )
        
        self.delete('food')
        self.delete('snake')
        
        if snake_game.food.coord is not None:
            self.draw_pixel(
                snake_game.food.coord,
                size / GAME_GRID,
                RED_COLOR,
                'food'
            )
        
        for snake_coord in snake_game.snake.coords:
            self.draw_pixel(
                snake_coord, 
                size / GAME_GRID, 
                BLUE_COLOR,
                'snake'
            )
    
    def draw_neural_network(self, neural_network: 'NeuralNetwork'):
        size = self.get_size()
        
        layers = [
            neural_network.input_layer, 
            *neural_network.hidden_layers, 
            neural_network.output_layer
        ]
        
        neurons = [neuron for layer in layers for neuron in layer.neurons]

        if all(len(self.find_withtag(i)) == 0 for i in ['neuron', 'line', 'text']):
            max_layer_len = max([len(layer.neurons) for layer in layers])
            layers_len = len(layers)
            
            width = NEURON_SIZE * layers_len
            height = NEURON_SIZE * max_layer_len
            
            x_margin = (size - width) / (layers_len - 1)
            y_margin = (size - height) / (max_layer_len - 1)

            prev_elements: list[int] = []
            elements: list[int] = []
            
            for layer_idx, layer in enumerate(layers):
                neurons_len = len(layer.neurons)
                
                layer_height = neurons_len * NEURON_SIZE + (neurons_len - 1) * y_margin
                
                top = (size - layer_height) / 2

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
        
        neuron_elements = self.find_withtag('neuron')
        text_elements = self.find_withtag('text')
        line_elements = self.find_withtag('line')
        
        neuron_elements_active: list[int] = []

        for i, neuron in enumerate(neurons):
            color = RED_COLOR if neuron.output > 0 else DARK_COLOR
            text = f'{neuron.output:.1f}' if neuron.output <= 99.9 else '99.9+'

            if neuron.output > 0:
                neuron_elements_active.append(neuron_elements[i])
            
            self.itemconfig(neuron_elements[i], fill=color)
            self.itemconfig(text_elements[i], text=text)

        for line_element in line_elements:
            line_coords = self.coords(line_element)

            elements_at_line: list[int] = [
                *self.find_overlapping(*line_coords[:2], *line_coords[:2]),
                *self.find_overlapping(*line_coords[2:], *line_coords[2:])
            ]

            elements_active_at_line = set(neuron_elements_active) & set(elements_at_line)
            
            color = RED_COLOR if len(elements_active_at_line) >= 2 else DARK_COLOR

            self.itemconfig(line_element, fill=color)

            if len(elements_active_at_line) >= 2:
                self.lift(line_element)

        for neuron_element in neuron_elements:
            self.lift(neuron_element)
        
        for text_element in text_elements:
            self.lift(text_element)