from tkinter import Canvas

from neural_network.layer import Layer
from neural_network.custom_types import Coord

from neural_network.config import NEURON_SIZE, NEURAL_NETWORK_WIDTH, NEURAL_NETWORK_HEIGHT, NEURON_HORIZONTAL_MARGIN, NEURON_VERTICAL_MARGIN, NEURON_CONNECTION_SIZE, NEURON_CENTER_SIZE

class UI:
    @staticmethod
    def draw_text(canvas: Canvas, coord: Coord, text: str, tag: str):
        return canvas.create_text(coord[0], coord[1], text=text, font=('Minecraft', 8), tags=tag, fill='#fff')
    
    @staticmethod
    def draw_line(canvas: Canvas, origin: Coord, destiny: Coord, fill: str, tag: str):
        return canvas.create_line(origin[0], origin[1], destiny[0], destiny[1], width=NEURON_CONNECTION_SIZE, tags=tag, fill=fill)
    
    @staticmethod
    def draw_neuron(canvas: Canvas, coord: Coord, fill: str, tag: str):
        return canvas.create_oval(
            coord[0],
            coord[1],
            coord[0] + NEURON_SIZE,
            coord[1] + NEURON_SIZE,
            fill=fill,
            width=0,
            tags=tag)
    
    @staticmethod
    def draw_layer(
        canvas: Canvas, 
        layer: Layer, 
        prev_layer: Layer | None, 
        layer_idx: int, 
        left: int, 
        neural_elements: list[list],
        text_elements: list
    ):
        layer_size = len(layer.neurons)
        vertical_size = NEURON_SIZE * layer_size + NEURON_VERTICAL_MARGIN * (layer_size - 1)
        top = int((NEURAL_NETWORK_HEIGHT - vertical_size) / 2)
        
        layer_elements: list = []
        
        for neuron_idx, neuron in enumerate(layer.neurons):
            x = left + layer_idx * NEURON_SIZE + layer_idx * NEURON_HORIZONTAL_MARGIN
            y = top + neuron_idx * NEURON_SIZE + neuron_idx * NEURON_VERTICAL_MARGIN
            
            neuron_color = 'red' if neuron.output > 0 else 'black'
            
            text_element = UI.draw_text(
                canvas, 
                [x + NEURON_CENTER_SIZE, y + NEURON_CENTER_SIZE], 
                f'{neuron.output:.1f}', 
                'neuron_text'
            )
            
            text_elements.append(text_element)
            
            neural_element = UI.draw_neuron(canvas, [x, y], neuron_color, 'neuron')
            
            if layer_idx != 0 and prev_layer is not None:
                for i, element in enumerate(neural_elements[-1]):
                    output = prev_layer.neurons[i].output
                    
                    element_x, element_y, *_ = canvas.coords(element)
                    
                    origin: list[float] = [x + NEURON_CENTER_SIZE, y + NEURON_CENTER_SIZE]
                    destiny = [element_x + NEURON_CENTER_SIZE, element_y + NEURON_CENTER_SIZE]
                    
                    line_color = 'red' if output > 0 and neuron.output > 0 else 'black'
                    
                    UI.draw_line(canvas, origin, destiny, line_color, 'line')
            
            layer_elements.append(neural_element)
        neural_elements.append(layer_elements)
        
    @staticmethod
    def draw_neural_network(canvas: Canvas, neural_network):
        canvas.delete('all')
        
        layers: list[Layer] = [
            neural_network.input_layer, 
            *neural_network.hidden_layers, 
            neural_network.output_layer
        ]
        
        layers_size = len(layers)
        horizontal_size = NEURON_SIZE * layers_size + NEURON_HORIZONTAL_MARGIN * (layers_size - 1)
        left = int((NEURAL_NETWORK_WIDTH - horizontal_size) / 2)
        
        neural_elements: list[list] = []
        text_elements: list = []
        
        for layer_idx, layer in enumerate(layers):
            prev_layer = layers[layer_idx - 1] if layer_idx != 0 else None
            UI.draw_layer(canvas, layer, prev_layer, layer_idx, left, neural_elements, text_elements)
            
        for layer_elements in neural_elements:
            for neuron_element in layer_elements:
                canvas.lift(neuron_element)
                
        for text_element in text_elements:
            canvas.lift(text_element)