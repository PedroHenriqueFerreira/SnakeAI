from neural_network.random import Random
from neural_network.neuron import Neuron

from config import *

class Layer:
    def __init__(
        self, 
        layer_size: int, 
        prev_layer_size: int | None = None, 
        is_output_layer: bool = False
    ):
        self.neurons: list[Neuron] = []
        
        self.layer_size = layer_size
        self.prev_layer_size = prev_layer_size
    
        self.is_output_layer = is_output_layer
            
        self.init_neurons()
        self.init_weights()

    def init_neurons(self):
        bias = 0 if self.is_output_layer else BIAS

        for _ in range(self.layer_size + bias):
            self.neurons.append(Neuron())

    def init_weights(self):
        if self.prev_layer_size is None: return

        neurons = self.neurons if self.is_output_layer else self.neurons[:-BIAS]

        for neuron in neurons:
            weights: list[float] = []
            
            for _ in range(self.prev_layer_size + BIAS):
                weights.append(Random.generate_number())
    
            neuron.wheights = weights

    def set_output(self, output: list[float]):
        for i in range(self.layer_size):
            self.neurons[i].output = output[i]  