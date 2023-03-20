from neural_network.neuron import Neuron
from neural_network.random_value import RandomValue
from neural_network.custom_types import LayerType

from neural_network.config import BIAS

class Layer:
    def __init__(self, layer_size: int, type: LayerType, prev_layer_size: int | None = None):
        self.neurons: list[Neuron] = []
        self.layer_size = layer_size
        self.prev_layer_size = prev_layer_size
        self.type = type
            
        self.init_neurons()
        self.init_weights()

    def init_neurons(self):
        bias = 0 if self.type == 'output' else BIAS

        for i in range(self.layer_size + bias):
            self.neurons.append(Neuron())

    def init_weights(self):
        if self.prev_layer_size is None: return

        neurons = self.neurons if self.type == 'output' else self.neurons[:-1]

        for neuron in neurons:
            neuron.wheights = [RandomValue.get_value() for _ in range(self.prev_layer_size + BIAS)]

    def set_output(self, output: list[float]):
        for i in range(self.layer_size):
            self.neurons[i].output = output[i]