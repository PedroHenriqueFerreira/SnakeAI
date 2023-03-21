class Neuron:
    def __init__(self):
        self.wheights: list[float] | None = None
        self.error = 0.0
        self.output = 1.0