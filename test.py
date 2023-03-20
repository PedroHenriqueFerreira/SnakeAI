from tkinter import Tk, Canvas

from neural_network import NeuralNetwork

from neural_network.UI import UI
from neural_network.config import NEURAL_NETWORK_WIDTH, NEURAL_NETWORK_HEIGHT

root = Tk()
canvas = Canvas(width=NEURAL_NETWORK_WIDTH, height=NEURAL_NETWORK_HEIGHT)
canvas.pack(expand=1)

neural = NeuralNetwork(2, [5], 4, 'relu')

UI.draw_neural_network(canvas, neural)

root.mainloop()