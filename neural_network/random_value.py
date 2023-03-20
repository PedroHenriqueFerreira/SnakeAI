from random import randint

class RandomValue:
    @staticmethod
    def get_value():
        return (randint(0, 20000) / 10.0) - 1000.0
    
    @staticmethod
    def get_medium_value():
        return RandomValue.get_value() / 100.0
    
    @staticmethod
    def get_small_value():
        return (randint(0, 10000) / 10000.0) + 0.5