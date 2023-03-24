from tkinter import Canvas
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from utils import Utils

from config import NEURON_FONT_CONFIG, LINE_WIDTH, CIRCLE_SIZE, BLACK_COLOR, WHITE_COLOR, CHART_SIZE, CHART_GRID, GRAY_COLOR, NEURAL_NETWORK_SIZE, BLUE_COLOR, GREEN_COLORS, BEST_PLAYER_SIZE, GAME_GRID

from custom_types import Coord

from neural_network import Neuron, NeuralNetwork


class UI:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw_pixel(self, coord: Coord, size: float, color: str, tag: str):
        return self.canvas.create_rectangle(
            coord[0] * size,
            coord[1] * size,
            (coord[0] + 1) * size,
            (coord[1] + 1) * size,
            width=0,
            fill=color,
            tags=tag
        )

    def draw_text(self, coord: Coord, color: str, text: str, font: tuple[str, int], tag: str):
        return self.canvas.create_text(
            coord[0],
            coord[1],
            text=text,
            font=font,
            fill=color,
            tags=tag
        )

    def draw_line(self, origin: Coord, destiny: Coord, color: str, tag: str):
        return self.canvas.create_line(
            origin[0],
            origin[1],
            destiny[0],
            destiny[1],
            width=LINE_WIDTH,
            fill=color,
            tags=tag
        )

    def draw_circle(self, coord: Coord, color: str, tag: str):
        return self.canvas.create_oval(
            coord[0],
            coord[1],
            coord[0] + CIRCLE_SIZE,
            coord[1] + CIRCLE_SIZE,
            fill=color,
            width=0,
            tags=tag)

    def draw_polygon(self, coords: list[Coord], color: str, tag: str):
        flat_coords = [pos for coord in coords for pos in coord]

        return self.canvas.create_polygon(
            *flat_coords,
            fill='',
            width=LINE_WIDTH,
            outline=color,
            tags=tag
        )

    def draw_neural_network(self, neural_network: NeuralNetwork):
        layers = [
            neural_network.input_layer,
            *neural_network.hidden_layers,
            neural_network.output_layer
        ]

        elements: list[list[int]] = []

        max_layer_size = max([len(layer.neurons) for layer in layers])
        VERTICAL_MARGIN = (NEURAL_NETWORK_SIZE - CIRCLE_SIZE *
                           max_layer_size) / (max_layer_size - 1)
        HORIZONTAL_MARGIN = (NEURAL_NETWORK_SIZE -
                             CIRCLE_SIZE * len(layers)) / (len(layers) - 1)

        for layer_idx, layer in enumerate(layers):
            row: list[int] = []

            vertical_size = Utils.get_total_size(
                CIRCLE_SIZE, len(layer.neurons), VERTICAL_MARGIN)
            top = int((NEURAL_NETWORK_SIZE - vertical_size) / 2)

            for neuron_idx, neuron in enumerate(layer.neurons):
                x = layer_idx * CIRCLE_SIZE + layer_idx * HORIZONTAL_MARGIN
                y = top + neuron_idx * CIRCLE_SIZE + neuron_idx * VERTICAL_MARGIN

                neuron_element = self.draw_circle(
                    [x, y], BLACK_COLOR, 'neuron')

                row.append(neuron_element)

                self.draw_text(
                    [pos + CIRCLE_SIZE / 2 for pos in [x, y]],
                    WHITE_COLOR,
                    '0.0',
                    NEURON_FONT_CONFIG,
                    'text'
                )

                if layer_idx == 0 or neuron.wheights is None:
                    continue

                for idx in range(len(neuron.wheights)):
                    destiny_coords = self.canvas.coords(
                        elements[layer_idx - 1][idx])[:2]
                    origin_coords = [x, y]

                    origin = [pos + CIRCLE_SIZE / 2 for pos in origin_coords]
                    destiny = [pos + CIRCLE_SIZE / 2 for pos in destiny_coords]

                    self.draw_line(origin, destiny, BLACK_COLOR, 'line')

            elements.append(row)

        for neuron_element in self.canvas.find_withtag('neuron'):
            self.canvas.lift(neuron_element)

        for text_element in self.canvas.find_withtag('text'):
            self.canvas.lift(text_element)

    def update_neural_network(self, neural_network: NeuralNetwork):
        layers = [neural_network.input_layer, *
                  neural_network.hidden_layers, neural_network.output_layer]

        neuron_elements_active: list[int] = []

        neuron_elements = self.canvas.find_withtag('neuron')
        text_elements = self.canvas.find_withtag('text')
        line_elements = self.canvas.find_withtag('line')

        neurons: list[Neuron] = []
        for layer in layers:
            neurons.extend(layer.neurons)

        for idx, neuron in enumerate(neurons):
            color = BLACK_COLOR

            if neuron.output > 0:
                color = BLUE_COLOR
                neuron_elements_active.append(neuron_elements[idx])

            self.canvas.itemconfig(neuron_elements[idx], fill=color)
            self.canvas.itemconfig(
                text_elements[idx], text=Utils.number_to_string(neuron.output))

        for line_element in line_elements:
            line_coords = self.canvas.coords(line_element)

            elements_at_start = self.canvas.find_overlapping(
                *line_coords[:2], *line_coords[:2])
            elements_at_end = self.canvas.find_overlapping(
                *line_coords[2:], *line_coords[2:])

            neuron_elements_over_line = list(
                (set(elements_at_start) | set(elements_at_end)) &
                set(neuron_elements_active)
            )

            color = BLUE_COLOR if len(
                neuron_elements_over_line) >= 2 else BLACK_COLOR

            self.canvas.itemconfig(line_element, fill=color)

            if len(neuron_elements_over_line) >= 2:
                self.canvas.lift(line_element)

        for neuron_element in neuron_elements:
            self.canvas.lift(neuron_element)

        for text_element in text_elements:
            self.canvas.lift(text_element)

    def draw_chart(self):
        BLOCK_SIZE = CHART_SIZE / CHART_GRID

        for index in range(CHART_GRID + 1):
            self.draw_line([0, index * BLOCK_SIZE], [CHART_SIZE,
                           index * BLOCK_SIZE], GRAY_COLOR, 'line')
            self.draw_line([index * BLOCK_SIZE, 0], [index *
                           BLOCK_SIZE, CHART_SIZE], GRAY_COLOR, 'line')

    def update_chart(self, data: list[int]):
        if len(data) == 0 or max(data) == 0:
            return

        coords: list[Coord] = []

        data = data[:]

        while len(data) < 100:
            data.insert(0, 0)
        while len(data) > 100:
            data.pop(0)

        for i, value in enumerate(data):
            x = i * (CHART_SIZE / (len(data) - 1))

            y = CHART_SIZE + LINE_WIDTH - (value / max(data)) * CHART_SIZE

            if len(data) - 1 == i:
                x += LINE_WIDTH

            coords.append([x, y])

        start_coord: Coord = [-LINE_WIDTH, CHART_SIZE + LINE_WIDTH]
        destiny_coord: Coord = [CHART_SIZE +
                                LINE_WIDTH, CHART_SIZE + LINE_WIDTH]

        self.clear('chart')
        self.draw_polygon(
            [start_coord, *coords, destiny_coord], BLUE_COLOR, 'chart')

    def draw_best_game(self, game: 'Game'):
        self.draw_pixel([0, 0], BEST_PLAYER_SIZE, GREEN_COLORS[0], 'bg')
        
        for i in range(2):
            for x in range(i, GAME_GRID, 2):
                for y in range(1 - i, GAME_GRID, 2):
                    self.draw_pixel(
                        [x, y],
                        BEST_PLAYER_SIZE / GAME_GRID,
                        GREEN_COLORS[1],
                        'bg'
                    )

    def clear(self, tag_or_id: str | int):
        self.canvas.delete(tag_or_id)

    def find(self, tag_or_id: str | int):
        return self.canvas.find_withtag(tag_or_id)