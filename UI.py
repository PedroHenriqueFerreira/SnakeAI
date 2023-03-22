from tkinter import Canvas
from random import randint

from utils import Utils

from config import GAME_SIZE, GAME_GRID, NEURON_FONT_CONFIG, LINE_WIDTH, CIRCLE_SIZE, NEURON_HORIZONTAL_MARGIN, NEURON_VERTICAL_MARGIN, RED_COLOR, DARK_COLOR, LIGHT_COLOR, GREEN_COLORS

from custom_types import Coord

from neural_network import Neuron, NeuralNetwork

class UI:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
    
    def draw_bg(self, color: str, tag: str):
        return self.canvas.create_rectangle(
            0,
            0,
            GAME_SIZE,
            GAME_SIZE,
            fill=color,
            width=0,
            tags=tag
        )
        
    def draw_pixel(self, coord: Coord, color: str, tag: str):
        pixel_size = GAME_SIZE / GAME_GRID
        
        return self.canvas.create_rectangle(
            coord[0] * pixel_size,
            coord[1] * pixel_size,
            (coord[0] + 1) * pixel_size,
            (coord[1] + 1) * pixel_size,
            fill=color,
            width=0,
            tags=tag
        )
        
    def draw_text(self, coord: Coord, color: str, text: str, font: tuple[str, int], tag: str):
        return self.canvas.create_text(
            coord[0],
            coord[1],
            text=text,
            font=font,
            fill=color,
            tags=tag
        )
        
    def draw_line(self, origin: Coord, destiny: Coord, color: str, tag: str):
        return self.canvas.create_line(
            origin[0], 
            origin[1], 
            destiny[0], 
            destiny[1], 
            width=LINE_WIDTH, 
            fill=color, 
            tags=tag
        )

    def draw_circle(self, coord: Coord, color: str, tag: str):
        return self.canvas.create_oval(
            coord[0],
            coord[1],
            coord[0] + CIRCLE_SIZE,
            coord[1] + CIRCLE_SIZE,
            fill=color,
            width=0,
            tags=tag)
        
    def draw_neural_network(self, neural_network: NeuralNetwork):
        layers = [
            neural_network.input_layer, 
            *neural_network.hidden_layers, 
            neural_network.output_layer
        ]

        elements: list[list[int]] = []
        
        for layer_idx, layer in enumerate(layers):
            row: list[int] = []
            
            vertical_size = Utils.get_total_size(CIRCLE_SIZE, len(layer.neurons), NEURON_VERTICAL_MARGIN)
            top = int((Utils.get_neural_network_height() - vertical_size) / 2)

            for neuron_idx, neuron in enumerate(layer.neurons):
                x = layer_idx * CIRCLE_SIZE + layer_idx * NEURON_HORIZONTAL_MARGIN
                y = top + neuron_idx * CIRCLE_SIZE + neuron_idx * NEURON_VERTICAL_MARGIN
                    
                neuron_element = self.draw_circle([x, y], DARK_COLOR, 'neuron')
                
                row.append(neuron_element)
                
                self.draw_text(
                    [pos + CIRCLE_SIZE / 2 for pos in [x, y]], 
                    RED_COLOR, 
                    '0.0', 
                    NEURON_FONT_CONFIG, 
                    'text'
                )
                
                if layer_idx == 0 or neuron.wheights is None: continue
                    
                for idx in range(len(neuron.wheights)):
                    xi, yi, *_ = self.canvas.coords(elements[layer_idx - 1][idx])

                    origin = [pos + CIRCLE_SIZE / 2 for pos in [x, y]]
                    destiny = [pos + CIRCLE_SIZE / 2 for pos in [xi, yi]]

                    self.draw_line(origin, destiny, DARK_COLOR, 'line')
                    
            elements.append(row)
            
        elements.clear()

        for neuron_element in self.canvas.find_withtag('neuron'):
            self.canvas.lift(neuron_element)
            
        for text_element in self.canvas.find_withtag('text'):
            self.canvas.lift(text_element)
    
    def update_neural_network(self, neural_network: NeuralNetwork):
        layers = [neural_network.input_layer, *neural_network.hidden_layers, neural_network.output_layer]
        
        neuron_elements_active: list[int] = []
        
        neuron_elements = self.canvas.find_withtag('neuron')
        text_elements = self.canvas.find_withtag('text')
        line_elements = self.canvas.find_withtag('line')
        
        neurons: list[Neuron] = []
        for layer in layers: neurons.extend(layer.neurons)
        
        for idx, neuron in enumerate(neurons):
            color = DARK_COLOR 
            
            if neuron.output > 0:
                color = RED_COLOR
                neuron_elements_active.append(neuron_elements[idx])
        
            self.canvas.itemconfig(neuron_elements[idx], fill=color)
            self.canvas.itemconfig(text_elements[idx], fill=LIGHT_COLOR, text=Utils.number_to_string(neuron.output))
        
        for line_element in line_elements:
            line_coords = self.canvas.coords(line_element)
            
            elements_at_start = self.canvas.find_overlapping(*line_coords[:2], *line_coords[:2])
            elements_at_end = self.canvas.find_overlapping(*line_coords[2:], *line_coords[2:])
            
            neuron_elements_over_line = list(
                (set(elements_at_start) | set(elements_at_end)) & 
                set(neuron_elements_active)
            )
            
            color = RED_COLOR if len(neuron_elements_over_line) >= 2 else DARK_COLOR
            
            self.canvas.itemconfig(line_element, fill=color)
            
            if (color == RED_COLOR): self.canvas.lift(line_element)
        
        for neuron_element in neuron_elements:
            self.canvas.lift(neuron_element)
            
        for text_element in text_elements:
            self.canvas.lift(text_element)
            
    def draw_grafic(self):
        for i in range(10):
            self.draw_line([0, i * 50], [500, i * 50], '#ccc', 'grafic')
            
        for i in range(10):
            self.draw_line([i * 50, 0], [i * 50, 500], '#ccc', 'grafic')
        
        dados = []    
        
        for i in range(50):
            rand = randint(50, 100)
            dados.append(rand)
            
        for i in range(50):
            rand = randint(100, 200)
            dados.append(rand)
        
        for i in range(50):
            rand = randint(200, 300)
            dados.append(rand)
        
        for i in range(len(dados)):
            width = 500 / len(dados)
            
            self.canvas.create_rectangle(i * width, 500, i * width + width, 500 - dados[i], fill=GREEN_COLORS[0], width=0)
            
            if i != len(dados) - 1:
                self.canvas.create_line((i + 0.5) * width, 500 - dados[i], (i + 1.5) * width, 500 - dados[i + 1], fill=DARK_COLOR, tags='line', width=2)
        
        for element in self.canvas.find_withtag('line'):
            self.canvas.lift(element)
            
    def clear(self, tag: str):
        self.canvas.delete(tag)