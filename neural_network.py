from random import randint

from utils import Utils

from custom_types import ActivationFunction, DNA

from config import NEURAL_NETWORK_BIAS

class Neuron:
    def __init__(self):
        self.wheights: list[float] | None = None
        self.output = 1.0

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
        bias = 0 if self.is_output_layer else NEURAL_NETWORK_BIAS

        for i in range(self.layer_size + bias):
            self.neurons.append(Neuron())

    def init_weights(self):
        if self.prev_layer_size is None: return

        neurons = self.neurons if self.is_output_layer else self.neurons[:-1]

        for neuron in neurons:
            weights: list[float] = []
            
            for _ in range(self.prev_layer_size + NEURAL_NETWORK_BIAS):
                weights.append(Utils.get_random_number())
    
            neuron.wheights = weights

    def set_output(self, output: list[float]):
        for i in range(self.layer_size):
            self.neurons[i].output = output[i]  

class NeuralNetwork:
    def __init__(
        self, 
        input_layer_size: int, 
        hidden_layer_sizes: list[int], 
        output_layer_size: int, 
        activation_function: ActivationFunction = Utils.relu,
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

    def generate_DNA_mutation(self, dna: DNA):
        random_mutations = randint(0, len(dna) - 1)
        
        for _ in range(random_mutations):
            random_operation = randint(0, 3)
            random_index = randint(0, len(dna) - 1)
            
            match random_operation:
                case 0:
                    dna[random_index] = Utils.get_random_number()
                case 1:
                    dna[random_index] *= Utils.get_small_random_number()
                case 2:
                    dna[random_index] += Utils.get_medium_random_number()
                case 3:
                    dna[random_index] -= Utils.get_medium_random_number()

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