from tkinter import Canvas, Event

from neural_network import NeuralNetwork

from UI import UI

from game.food import Food
from game.snake import Snake

from config import *

class SnakeGame:
    def __init__(
        self, 
        game_canvas: Canvas, 
        best_game_canvas: Canvas, 
        is_AI: bool = False
    ):
        self.UI = UI(game_canvas)
        self.best_game_UI = UI(best_game_canvas)

        self.draw_bg()

        self.snake = Snake(self)
        self.food = Food(self)

        self.is_paused = True

        self.brain: NeuralNetwork | None = None
        
        self.create_message('Jogar Snake')

        if not is_AI:
            keys = ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']

            for key in keys:
                game_canvas.bind(key, self.key_event)

            game_canvas.focus_set()

    def key_event(self, event: Event):
        self.snake.change_direction(event.keysym)

        if self.is_paused:
            self.start()

    def start(self):
        self.is_paused = False

        self.remove_message()

        self.snake.reset()
        self.food.reset()

        self.move()

    def on_game_over(self):
        if self.snake.lives == 0:
            self.snake.score = 0
            self.snake.lives = LIVES
        
        current_score = self.snake.get_score()
        
        if (current_score > self.snake.score):
            self.snake.score = current_score
        
        self.snake.lives -= 1
        
        if self.snake.lives > 0:
            return self.start()

        self.is_paused = True

        self.create_message(f'Pontuacao: {self.snake.score}')

    def move(self):
        if self.is_paused:
            return

        snake_head = self.snake.coords[-1][:]

        match(self.snake.direction):
            case 'up': snake_head[1] -= 1
            case 'down': snake_head[1] += 1
            case 'left': snake_head[0] -= 1
            case 'right': snake_head[0] += 1

        isBodyColiding = snake_head in self.snake.coords
        isWallColiding = -1 in snake_head or GAME_GRID in snake_head

        if isBodyColiding or isWallColiding or self.snake.energy == 0:
            return self.on_game_over()

        self.snake.add_coord(snake_head)

        if snake_head == self.food.coord:
            self.food.reset()

            self.snake.energy = GAME_GRID ** 2
        else:
            self.snake.remove_tail()

            self.snake.energy -= 1

        self.UI.after(FPS, self.move)

    def get_available_coords(self):
        availableSpots: list[list[float]] = []

        for x in range(GAME_GRID):
            for y in range(GAME_GRID):
                coord: list[float] = [x, y]

                if coord in self.snake.coords:
                    continue

                availableSpots.append(coord)

        return availableSpots

    def draw_bg(self):
        self.UI.draw_pixel([0, 0], GAME_SIZE, GREEN_COLORS[0], 'bg')

        for i in range(2):
            for x in range(i, GAME_GRID, 2):
                for y in range(1 - i, GAME_GRID, 2):
                    self.UI.draw_pixel(
                        [x, y],
                        GAME_SIZE / GAME_GRID,
                        GREEN_COLORS[1],
                        'bg'
                    )

    def create_message(self, text: str):
        self.UI.draw_pixel(
            [0, 0],
            GAME_SIZE,
            BLACK_COLOR,
            'message'
        )

        self.UI.draw_text(
            [GAME_SIZE / 2, GAME_SIZE / 2],
            WHITE_COLOR,
            text,
            GAME_FONT,
            'message'
        )

    def remove_message(self):
        self.UI.clear('message')

    def get_food_distance(self):
        snake_head = self.snake.coords[-1]

        if self.food.coord is None:
            return [0, 0, 0, 0]

        data: list[int] = []

        for i in range(2):
            if self.food.coord[i] - snake_head[i] < 0:
                data.append(1)
                data.append(0)
            elif self.food.coord[i] - snake_head[i] > 0: 
                data.append(0)
                data.append(1)
            else:
                data.append(0)
                data.append(0)

        return data

    def get_close_objects(self):
        objects = []
        
        snake_head = self.snake.coords[-1]
        snake_neck = self.snake.coords[-2]
        
        for x in range(-1, 2):
            for y in range(-1, 2):
                coord = [snake_head[0] + x, snake_head[1] + y]
                
                if coord == snake_head or coord == snake_neck:
                    continue
                
                if coord in self.snake.coords or -1 in coord or GAME_GRID in coord:
                    objects.append(0)
                    objects.append(1)
                else:
                    objects.append(1)
                    objects.append(0)
                
        return objects

    def draw_best_game(self):
        self.best_game_UI.draw_pixel([0, 0], BEST_GAME_SIZE, GREEN_COLORS[0], 'bg')
        
        for i in range(2):
            for x in range(i, GAME_GRID, 2):
                for y in range(1 - i, GAME_GRID, 2):
                    self.best_game_UI.draw_pixel(
                        [x, y],
                        BEST_GAME_SIZE / GAME_GRID,
                        GREEN_COLORS[1],
                        'bg'
                    )

    def update_best_game(self):
        self.best_game_UI.clear('snake')
        self.best_game_UI.clear('food')
        
        if self.food.coord is not None:
            self.best_game_UI.draw_pixel(
                self.food.coord,
                BEST_GAME_SIZE / GAME_GRID,
                RED_COLOR,
                'food'
            )
        
        for snake_coord in self.snake.coords:
            self.best_game_UI.draw_pixel(
                snake_coord, 
                BEST_GAME_SIZE / GAME_GRID, 
                BLUE_COLOR,
                'snake'
            )