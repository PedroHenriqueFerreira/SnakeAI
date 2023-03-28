from tkinter import Canvas
from typing import Callable
from random import randint

from UI import UI

from neural_network.random import Random
from neural_network.layer import Layer

from config import *

class NeuralNetwork:
    def __init__(
        self, 
        canvas: Canvas,
        input_layer_size: int, 
        hidden_layer_sizes: list[int], 
        output_layer_size: int, 
        activation_function: Callable[[float], float]
    ):  
        self.UI = UI(canvas)
        
        self.input_layer_size = input_layer_size
        self.hidden_layer_sizes = hidden_layer_sizes
        self.output_layer_size = output_layer_size

        self.activation_function = activation_function

        self.input_layer, self.hidden_layers, self.output_layer = self.init_layers()

    def init_layers(self) -> tuple[Layer, list[Layer], Layer]:
        input_layer = Layer(self.input_layer_size)

        hidden_layers: list[Layer] = []

        for i, hidden_layer_size in enumerate(self.hidden_layer_sizes):
            prev_layer_size = self.input_layer_size if i == 0 else self.hidden_layer_sizes[i - 1]
            
            hidden_layers.append(Layer(hidden_layer_size, prev_layer_size))

        output_layer = Layer(self.output_layer_size, self.hidden_layer_sizes[-1], True)

        return input_layer, hidden_layers, output_layer

    def generate_DNA_mutation(self):
        dna = self.get_DNA()
        
        random_mutations = randint(0, len(dna) - 1)
        
        for _ in range(random_mutations):
            random_operation = randint(0, 4)
            random_index = randint(0, len(dna) - 1)
            
            match random_operation:
                case 0:
                    dna[random_index] = Random.generate_number()
                case 1:
                    dna[random_index] += Random.generate_number() / 100
                case 2:
                    dna[random_index] -= Random.generate_number() / 100
                case 3:
                    dna[random_index] *= Random.generate_tiny_number()
                case 4:
                    dna[random_index] /= Random.generate_tiny_number()

        self.set_DNA(dna)

    def get_DNA(self):
        dna: list[float] = []

        for layer in [*self.hidden_layers, self.output_layer]:
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                dna += neuron.wheights

        return dna

    def set_DNA(self, dna: list[float]):
        index = 0

        for layer in [*self.hidden_layers, self.output_layer]:
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                for i in range(len(neuron.wheights)):
                    neuron.wheights[i] = dna[index]
                    index += 1

    def calculate_output(self):
        for layer_index, layer in enumerate([*self.hidden_layers, self.output_layer]):
            prev_layer = self.input_layer if layer_index == 0 else self.hidden_layers[layer_index - 1]
            
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                output = 0.0
                for i, weight in enumerate(neuron.wheights):
                    output += weight * prev_layer.neurons[i].output                
                
                neuron.output = self.activation_function(output)
        
        return [neuron.output for neuron in self.output_layer.neurons]  

    def draw(self):
        layers = [self.input_layer, *self.hidden_layers, self.output_layer]

        elements: list[list[int]] = []

        max_layer_size = max([len(layer.neurons) for layer in layers])
        
        x_margin = (NEURAL_NETWORK_SIZE - NEURON_SIZE * len(layers)) / (len(layers) - 1)
        y_margin = (NEURAL_NETWORK_SIZE - NEURON_SIZE * max_layer_size) / (max_layer_size - 1)

        for layer_idx, layer in enumerate(layers):
            row: list[int] = []

            layer_size = len(layer.neurons)

            top = (NEURAL_NETWORK_SIZE - (layer_size * NEURON_SIZE + (layer_size - 1) * y_margin)) / 2

            for neuron_idx, neuron in enumerate(layer.neurons):
                x = layer_idx * NEURON_SIZE + layer_idx * x_margin
                y = top + neuron_idx * NEURON_SIZE + neuron_idx * y_margin

                neuron_element = self.UI.draw_circle([x, y], NEURON_SIZE, BLACK_COLOR, 'neuron')

                row.append(neuron_element)

                self.UI.draw_text(
                    [pos + NEURON_SIZE / 2 for pos in [x, y]],
                    WHITE_COLOR,
                    '0.0',
                    NEURON_FONT,
                    'text'
                )

                if layer_idx == 0 or neuron.wheights is None:
                    continue

                for neuron_idx in range(len(neuron.wheights)):
                    origin_coords = [x, y]
                    destiny_coords = self.UI.coords(elements[layer_idx - 1][neuron_idx])[:2]

                    origin = [pos + NEURON_SIZE / 2 for pos in origin_coords]
                    destiny = [pos + NEURON_SIZE / 2 for pos in destiny_coords]

                    self.UI.draw_line(origin, destiny, BLACK_COLOR, 'line')

            elements.append(row)

        self.UI.move_up('neuron')
        self.UI.move_up('text')
    
    def draw_update(self):
        layers = [self.input_layer, *self.hidden_layers, self.output_layer]
        neurons = [neuron for layer in layers for neuron in layer.neurons]
        
        neuron_elements = self.UI.find('neuron')
        text_elements = self.UI.find('text')
        line_elements = self.UI.find('line')
        
        neuron_elements_active: list[int] = []

        for i, neuron in enumerate(neurons):
            color = RED_COLOR if neuron.output > 0 else BLACK_COLOR

            if neuron.output > 0:
                neuron_elements_active.append(neuron_elements[i])

            text = f'{neuron.output:.1f}' if neuron.output < 100 else '99.9+'
            
            self.UI.element_config(neuron_elements[i], fill=color)
            self.UI.element_config(text_elements[i], text=text)

        for line_element in line_elements:
            line_coords = self.UI.coords(line_element)

            elements: list[int] = []
            
            elements += self.UI.find_at_coord(line_coords[:2])
            elements += self.UI.find_at_coord(line_coords[2:])

            elements = set(neuron_elements_active) & set(elements)
            
            color = RED_COLOR if len(elements) >= 2 else BLACK_COLOR

            self.UI.element_config(line_element, fill=color)

            if len(elements) >= 2:
                self.UI.move_up(line_element)

        self.UI.move_up('neuron')
        self.UI.move_up('text')