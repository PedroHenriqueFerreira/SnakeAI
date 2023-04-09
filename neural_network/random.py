from random import randint

class Random:
    @staticmethod
    def get_number():
        return (randint(0, 20000) / 10) - 1000
    
    @staticmethod
    def get_tiny_number():
        return (randint(0, 10000) / 10000) + 0.5