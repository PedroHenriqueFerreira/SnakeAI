from neural_network.random_value import RandomValue

class Neuron:
    def __init__(self):
        self.wheights: list[float] = []
        self.error = 0.0
        self.output = 1.0