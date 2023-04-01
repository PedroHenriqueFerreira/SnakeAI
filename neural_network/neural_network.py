from typing import Callable
from random import randint

from neural_network.random import Random
from neural_network.layer import Layer

class NeuralNetwork:
    def __init__(
        self, 
        input_layer_size: int, 
        hidden_layer_sizes: list[int], 
        output_layer_size: int, 
        activation_function: Callable[[float], float]
    ):  
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
        DNA = self.get_DNA()
        
        random_mutations = randint(0, len(DNA) - 1)
        
        for _ in range(random_mutations):
            random_operation = randint(0, 4)
            random_idx = randint(0, len(DNA) - 1)
            
            match random_operation:
                case 0:
                    DNA[random_idx] = Random.generate_number()
                case 1:
                    DNA[random_idx] += Random.generate_number() / 100
                case 2:
                    DNA[random_idx] -= Random.generate_number() / 100
                case 3:
                    DNA[random_idx] *= Random.generate_tiny_number()
                case 4:
                    DNA[random_idx] /= Random.generate_tiny_number()

        self.set_DNA(DNA)

    def get_DNA(self):
        DNA: list[float] = []

        for layer in [*self.hidden_layers, self.output_layer]:
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                DNA += neuron.wheights

        return DNA

    def set_DNA(self, DNA: list[float]):
        idx = 0

        for layer in [*self.hidden_layers, self.output_layer]:
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                for i in range(len(neuron.wheights)):
                    neuron.wheights[i] = DNA[idx]
                    idx += 1

    def calculate_output(self):
        for layer_idx, layer in enumerate([*self.hidden_layers, self.output_layer]):
            prev_layer = self.input_layer if layer_idx == 0 else self.hidden_layers[layer_idx - 1]
        
        for layer_idx, layer in enumerate([*self.hidden_layers, self.output_layer]):
            prev_layer = self.input_layer if layer_idx == 0 else self.hidden_layers[layer_idx - 1]
            
            for neuron in layer.neurons:
                if neuron.wheights is None: continue
                
                output = 0.0
                for i, weight in enumerate(neuron.wheights):
                    output += weight * prev_layer.neurons[i].output                
                
                neuron.output = self.activation_function(output)
        
        return [neuron.output for neuron in self.output_layer.neurons]  