from tkinter import Tk, Canvas
from math import exp
from typing import Callable

from random import randint

from neural_network.UI import UI
from neural_network.layer import Layer

from neural_network.random_value import RandomValue

from neural_network.custom_types import DNA, Activation

class NeuralNetwork:
    def __init__(
        self, 
        input_layer_size: int, 
        hidden_layer_sizes: list[int], 
        output_layer_size: int, 
        activation: Activation = 'relu',
    ):  
        self.input_layer_size = input_layer_size
        self.hidden_layer_sizes = hidden_layer_sizes
        self.output_layer_size = output_layer_size
        
        self.activation_function = { 'sigmoid': self.sigmoid, 'relu': self.relu }[activation]

        self.input_layer, self.hidden_layers, self.output_layer = self.init_layers()

    def init_layers(self) -> tuple[Layer, list[Layer], Layer]:
        input_layer = Layer(self.input_layer_size, 'input')

        hidden_layers: list[Layer] = []

        for i, hidden_layer_size in enumerate(self.hidden_layer_sizes):
            prev_layer_size = self.input_layer_size if i == 0 else self.hidden_layer_sizes[i - 1]
            hidden_layers.append(Layer(hidden_layer_size, 'hidden', prev_layer_size))

        output_layer = Layer(self.output_layer_size, 'output', self.hidden_layer_sizes[-1])

        return input_layer, hidden_layers, output_layer

    def generate_DNA_mutation(self, dna: DNA):
        random_mutations = randint(0, len(dna) - 1)
        
        for _ in range(random_mutations):
            random_operation = randint(0, 3)
            random_index = randint(0, len(dna) - 1)
            
            match random_operation:
                case 0:
                    dna[random_index] = RandomValue.get_value()
                case 1:
                    dna[random_index] *= RandomValue.get_small_value()
                case 2:
                    dna[random_index] += RandomValue.get_medium_value()
                case 3:
                    dna[random_index] -= RandomValue.get_medium_value()

        self.set_DNA(dna)

    def get_DNA(self) -> DNA:
        dna: DNA = []

        for layer in [*self.hidden_layers, self.output_layer]:
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                dna.extend(neuron.wheights)

        return dna

    def set_DNA(self, dna: DNA):
        dnaIndex = 0

        for layer in [*self.hidden_layers, self.output_layer]:
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                for i in range(len(neuron.wheights)):
                    neuron.wheights[i] = dna[dnaIndex]
                    dnaIndex += 1

    def calculate_output(self):
        for idx, layer in enumerate([*self.hidden_layers, self.output_layer]):
            prev_layer = self.input_layer if idx == 0 else self.hidden_layers[idx - 1]
            
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                output = 0.0
                for i, weight in enumerate(neuron.wheights):
                    output += weight * prev_layer.neurons[i].output                
                
                neuron.output = self.activation_function(output)
        
        return [neuron.output for neuron in self.output_layer.neurons]  
    
    def relu(self, x: float): 
        return max(0, x)
    
    def sigmoid(self, x: float): 
        return 1 / (1 + exp(-x)) 