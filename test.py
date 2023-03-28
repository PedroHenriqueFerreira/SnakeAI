from game import SnakeGame
from neural_network import NeuralNetwork
from chart import Chart

from random import randint

from tkinter import Canvas, Tk
from config import *

root = Tk()

canvas = Canvas(root, width=GAME_SIZE, height=GAME_SIZE)
canvas.pack(expand=1)

SnakeGame(canvas, canvas)

# chart = Chart(canvas)

# chart.draw()

# chart.values = [5, 10]

# chart.draw_update()

# nn = NeuralNetwork(
#     canvas,
#     12, 
#     [10, 10], 
#     8, 
#     ACTIVATION_FUNCTION
# )

# nn.draw()

# def loop():
#     nn.generate_DNA_mutation()
#     nn.input_layer.set_output([randint(-10, 10) for _ in range(12)])
#     nn.calculate_output()
    
#     nn.draw_update()

#     # chart.values.append(randint(0, 1000))
#     # chart.draw_update()
    
#     root.update()
    
#     canvas.after(100, loop)
    
# canvas.after(100, loop)
    
root.mainloop()