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
    def __init__(self, neurons_amount: int, type: str, prev_amount: int | None = None):
        self.neurons: list[Neuron] = []
        self.neurons_amount = neurons_amount
        self.prev_amount = prev_amount
        self.type = type
            
        self.initNeurons()
        self.initWeights()

    def initNeurons(self):
        bias = BIAS if self.type != 'output' else 0

        for _ in range(self.neurons_amount + bias):
            self.neurons.append(Neuron())

    def initWeights(self):
        if self.type == 'input' or self.prev_amount is None:
            return

        neurons = self.neurons if self.type == 'output' else self.neurons[:-1]

        for neuron in neurons:
            neuron.wheights = [1.0 for _ in range(self.prev_amount + 1)]

relu = lambda x: max(0, x)

class NeuralNetwork(Default):
    def __init__(self, input_amount: int, hidden_amounts: list[int], output_amount: int, activation = relu):
        self.input_amount = input_amount
        self.hidden_amounts = hidden_amounts
        self.output_amount = output_amount
        self.activation = activation

        self.input_layer, self.hidden_layers, self.output_layer = self.initLayers()

    def initLayers(self) -> tuple[Layer, list[Layer], Layer]:
        input_layer = Layer(self.input_amount, 'input')

        hidden_layers: list[Layer] = []

        for i, hidden_amount in enumerate(self.hidden_amounts):
            prev_amount = self.input_amount if i == 0 else self.hidden_amounts[i - 1]
            hidden_layers.append(Layer(hidden_amount, 'hidden', prev_amount))

        output_layer = Layer(self.output_amount, 'output', self.hidden_amounts[i - 1])

        return input_layer, hidden_layers, output_layer

    def getDNA(self):
        dna: list[float] = []

        for layer in self.hidden_layers:
            for neuron in layer.neurons:
                if neuron.wheights is not None:
                    dna.extend(neuron.wheights)

        for neuron in self.output_layer.neurons:
            if neuron.wheights is not None:
                dna.extend(neuron.wheights)

        return dna

    def setRandomDNA(self):
        self.setDNA([randint(-1000, 1000) for _ in self.getDNA()])

    def setDNA(self, dna: list[float]):
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

    def calculateOutput(self):
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

NeuralNetwork(8, [6, 6, 6], 4)
