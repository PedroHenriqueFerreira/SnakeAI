from abc import ABC
from random import randint

BIAS = 1

class Default(ABC):
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__})'

    def __str__(self) -> str:
        return self.__repr__()

class Neuron(Default):
    def __init__(self, wheights: list[float] | None = None):
        self.wheights = wheights
        self.error = 0.0
        self.output = 1.0

class Layer(Default):
    def __init__(self, layer_size: int, type: str, prev_layer_size: int | None = None):
        self.neurons: list[Neuron] = []
        self.layer_size = layer_size
        self.prev_layer_size = prev_layer_size
        self.type = type
            
        self.init_neurons()
        self.init_weights()

    def init_neurons(self):
        bias = BIAS if self.type != 'output' else 0

        for _ in range(self.layer_size + bias):
            self.neurons.append(Neuron())

    def init_weights(self):
        if self.type == 'input' or self.prev_layer_size is None:
            return

        neurons = self.neurons if self.type == 'output' else self.neurons[:-1]

        for neuron in neurons:
            neuron.wheights = [1.0 for _ in range(self.prev_layer_size + 1)]

    def set_values(self, output: list[int]):
        for i in range(len(self.neurons) - BIAS):
            self.neurons[i].output = output[i]

relu = lambda x: max(0, x)

class NeuralNetwork(Default):
    def __init__(
        self, 
        input_layer_size: int, 
        hidden_layer_sizes: list[int], 
        output_layer_size: int, 
        activation = relu
    ):
        self.input_layer_size = input_layer_size
        self.hidden_layer_sizes = hidden_layer_sizes
        self.output_layer_size = output_layer_size
        self.activation = activation

        self.input_layer, self.hidden_layers, self.output_layer = self.init_layers()

    def init_layers(self) -> tuple[Layer, list[Layer], Layer]:
        input_layer = Layer(self.input_layer_size, 'input')

        hidden_layers: list[Layer] = []

        for i, hidden_layer_size in enumerate(self.hidden_layer_sizes):
            prev_layer_size = self.input_layer_size if i == 0 else self.hidden_layer_sizes[i - 1]
            hidden_layers.append(Layer(hidden_layer_size, 'hidden', prev_layer_size))

        output_layer = Layer(self.output_layer_size, 'output', self.hidden_layer_sizes[i - 1])

        return input_layer, hidden_layers, output_layer

    def get_DNA(self):
        dna: list[float] = []

        for layer in self.hidden_layers:
            for neuron in layer.neurons:
                if neuron.wheights is not None:
                    dna.extend(neuron.wheights)

        for neuron in self.output_layer.neurons:
            if neuron.wheights is not None:
                dna.extend(neuron.wheights)

        return dna

    def set_DNA(self, dna: list[float]):
        dnaIndex = 0

        for layer in self.hidden_layers:
            for neuron in layer.neurons:
                if neuron.wheights is not None:
                    for i in range(len(neuron.wheights)):
                        neuron.wheights[i] = dna[dnaIndex]
                        dnaIndex += 1

        for neuron in self.output_layer.neurons:
            if neuron.wheights is not None:
                for i in range(len(neuron.wheights)):
                    neuron.wheights[i] = dna[dnaIndex]
                    dnaIndex += 1

    def calculate_output(self):
        for idx, hidden_layer in enumerate(self.hidden_layers):
            prev_layer = self.input_layer if idx == 0 else self.hidden_layers[idx - 1]
            
            for neuron in hidden_layer.neurons:
                if neuron.wheights is None:
                    continue
                
                output = 0.0
                
                for i, weight in enumerate(neuron.wheights):
                    output += weight * prev_layer.neurons[i].output                
                    
                neuron.output = self.activation(output)
        
        for i, neuron in enumerate(self.output_layer.neurons):
            if neuron.wheights is None:
                continue
            
            output = 0.0
            for i, weight in enumerate(neuron.wheights):
                output += weight * self.hidden_layers[-1].neurons[i].output                
                
            neuron.output = self.activation(output)

        return [neuron.output for neuron in self.output_layer.neurons]