from math import exp
from random import randint

class Utils:
    @staticmethod
    def get_total_size(element_size: float, element_count: int, spacing: float):
        return element_count * element_size + (element_count - 1) * spacing
    
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