from tkinter import Tk, Canvas, Event
from neural_network import NeuralNetwork
from game_types import Direction, Pos

from constants import CANVAS_GRID, PIXEL_SIZE, CANVAS_SIZE, SPEED, FONT_CONFIG
from constants import NEURAL_INPUT_AMOUNT, NEURAL_HIDDEN_AMOUNT, NEURAL_OUTPUT_AMOUNT
from constants import BG_COLORS, MESSAGE_BG_COLOR

from snake import Snake
from food import Food

class Game:
    def __init__(self, win: Tk, canvas: Canvas):
        self.canvas = canvas
        
        self.brain = NeuralNetwork(
            NEURAL_INPUT_AMOUNT, 
            NEURAL_HIDDEN_AMOUNT, 
            NEURAL_OUTPUT_AMOUNT
        )
        
        self.create_bg()
        
        self.snake = Snake(canvas)
        self.food = Food(self, canvas)
        
        self.is_paused = True
        self.create_message('Jogar Snake')
        
        self.listen_keys(win)
    
    def listen_keys(self, win: Tk):    
        for key in ['<Up>', '<Right>', '<Down>', '<Left>', 'w', 'd', 's', 'a']:
            win.bind(key, self.key_event)

    def key_event(self, event: Event):
        key = event.keysym
        self.snake.change_direction(self.tranform_in_direction(key))
        
        if self.is_paused: self.start()
    
    def tranform_in_direction(self, key: str) -> Direction:
        match(key):
            case 'Up' | 'w':
                return 'up'
            case 'Right' | 'd':
                return 'right'
            case 'Down' | 's':
                return 'down'
            case 'Left' | 'a':
                return 'left'
            case _:
                return 'right'
    
    def start(self):
        self.is_paused = False
        
        self.remove_message()
        
        self.snake.reset()
        self.food.coord = self.food.move_coord()
        
        self.move()
        
    def game_over(self):
        self.is_paused = True
        
        self.create_message(f'Pontuacao: {self.snake.score}')
    
    def finished(self):
        self.is_paused = True
        
        self.create_message('Parabens!')
    
    def move(self):
        snakePos = self.snake.coords[-1][:]
        
        if (self.snake.direction == 'up'):
            snakePos[1] -= 1
        elif (self.snake.direction == 'down'):
            snakePos[1] += 1
        elif (self.snake.direction == 'left'):
            snakePos[0] -= 1
        elif (self.snake.direction == 'right'):
            snakePos[0] += 1
        
        self.snake.add_coord(snakePos)
        
        isBodyColiding = snakePos in self.snake.coords[:-1]
        isWallColiding = -1 in snakePos or CANVAS_GRID in snakePos
        
        if snakePos == self.food.coord:
            self.food.coord = self.food.move_coord()
            self.snake.score += 1
        elif isBodyColiding or isWallColiding: 
            return self.game_over()
        elif len(self.snake.coords) == CANVAS_GRID ** 2:
            return self.finished()
        else:
            self.snake.remove_coord()
            
        self.canvas.after(SPEED, self.move)
    
    def getAvailableSpots(self):
        availableSpots: list[Pos] = []

        for x in range(CANVAS_GRID):
            for y in range(CANVAS_GRID):
                pos = [x, y]
                
                if pos in self.snake.coords:
                    continue
                
                availableSpots.append(pos)

        return availableSpots
        
    def create_bg(self):
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill=BG_COLORS[0], width=0)
        
        for x in range(CANVAS_GRID):
            for y in range(CANVAS_GRID):
                if not ((x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0)):
                    continue
                
                self.canvas.create_rectangle(
                    x * PIXEL_SIZE,
                    y * PIXEL_SIZE, 
                    (x + 1) * PIXEL_SIZE,
                    (y + 1) * PIXEL_SIZE,
                    fill=BG_COLORS[1], 
                    width=0
                )
    def create_message(self, text: str):
        self.canvas.create_rectangle(0, 0, CANVAS_SIZE, CANVAS_SIZE, fill=MESSAGE_BG_COLOR, width=0, tags='message')
        
        self.canvas.create_text(
            CANVAS_SIZE / 2,
            CANVAS_SIZE / 2,
            text=text,
            font=FONT_CONFIG,
            fill='white',
            tags='message'
        )
    
    def remove_message(self):
        self.canvas.delete('message')

    def food_x_distance(self):
        return self.food.coord[0] - self.snake.coords[-1][0]

    def food_y_distance(self):
        return self.food.coord[1] - self.snake.coords[-1][1]