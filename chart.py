from tkinter import Canvas

from UI import UI

from config import *

class Chart:
    def __init__(self, canvas: Canvas):
        self.UI = UI(canvas)

    def draw(self):
        block_size = CHART_SIZE / CHART_GRID

        for i in range(CHART_GRID + 1):
            pos = i * block_size

            self.UI.draw_line([0, pos], [CHART_SIZE, pos], GRAY_COLOR, 'line')
            self.UI.draw_line([pos, 0], [pos, CHART_SIZE], GRAY_COLOR, 'line')

    def draw_update(self, values: list[float]):
        coords: list[list[float]] = []

        if values is None or len(values) == 0 or max(values) == 0:
            return
        
        values = values[:]

        if len(values) > 1:
            for i, value in enumerate(values):
                x = i * (CHART_SIZE / (len(values) - 1))

                y = CHART_SIZE + LINE_WIDTH - (value / max(values)) * CHART_SIZE

                if i == 0:
                    x -= LINE_WIDTH

                if i == len(values) - 1:
                    x += LINE_WIDTH

                coords.append([x, y])
        else:
            coords.append([0, CHART_SIZE])
            coords.append([CHART_SIZE, 0])

        start_coord: list[float] = [-LINE_WIDTH, -LINE_WIDTH]
        destiny_coord: list[float] = [CHART_SIZE + LINE_WIDTH, -LINE_WIDTH]

        self.UI.clear('chart')
        self.UI.draw_polygon([start_coord, *coords, destiny_coord], RED_COLOR, 'chart')
