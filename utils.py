from math import exp
from random import randint

from config import INPUT_LAYER_SIZE, HIDDEN_LAYER_SIZES, OUTPUT_LAYER_SIZE, CIRCLE_SIZE, NEURON_HORIZONTAL_MARGIN, NEURON_VERTICAL_MARGIN

class Utils:
    @staticmethod
    def get_total_size(element_size: int, element_count: int, spacing: int):
        return element_count * element_size + (element_count - 1) * spacing
    
    @staticmethod
    def get_neural_network_width():
        count = len([INPUT_LAYER_SIZE, *HIDDEN_LAYER_SIZES, OUTPUT_LAYER_SIZE])
        
        return count * CIRCLE_SIZE + (count - 1) * NEURON_HORIZONTAL_MARGIN
    
    @staticmethod
    def get_neural_network_height():
        count = max(
            max([INPUT_LAYER_SIZE, *HIDDEN_LAYER_SIZES]) + 1, 
            OUTPUT_LAYER_SIZE
        )
        
        return count * CIRCLE_SIZE + (count - 1) * NEURON_VERTICAL_MARGIN
    
    @staticmethod
    def number_to_string(number: float):
        return f'{number:.1f}' if number < 100 else '99.9+'
    
    @staticmethod
    def get_random_number():
        return (randint(0, 20000) / 10.0) - 1000.0
    
    @staticmethod
    def get_medium_random_number():
        return Utils.get_random_number() / 100.0
    
    @staticmethod
    def get_small_random_number():
        return (randint(0, 10000) / 10000.0) + 0.5
    
    @staticmethod
    def relu(x: float): 
        return max(0, x)
    
    @staticmethod
    def sigmoid(x: float): 
        return 1 / (1 + exp(-x)) 
    
    @staticmethod
    def step(x: float):
        return 1.0 if x > 0 else 0.0