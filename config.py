TITLE = 'Snake Game AI'

SPEED = 100
LIVES = 3

GAMES_ROW_GRID = 7
GAMES_COLUMN_GRID = 11

GAME_SIZE = 130
BEST_GAME_SIZE = 308
GAME_GRID = 20

CHART_SIZE = 308
CHART_GRID = 10

NEURAL_NETWORK_SIZE = 308
NEURON_SIZE = 23

PADDING = 5

LINE_WIDTH = 2

DEFAULT_FONT = ('Minecraft', 15)
GAME_FONT = ('Minecraft', int(GAME_SIZE / 11))
NEURON_FONT = ('Minecraft', int(NEURON_SIZE / 4))

BLUE_COLOR = '#4430BE'
GREEN_COLORS = ['#7ECE6A', '#87D973']
RED_COLOR = '#BE3049'
LIGHT_COLOR = '#FFF'
DARK_COLOR = '#373737'
BG_COLOR = '#292929'

INPUT_LAYER_SIZE = 12
HIDDEN_LAYER_SIZES = [8, 8]
OUTPUT_LAYER_SIZE = 4
ACTIVATION_FUNCTION = lambda x: max(0, x)

BEST_PLAYERS_SELECT = 3

RECORD_TEXT = 'Melhor pontuacao recorde: 0'
SCORE_TEXT = 'Melhor pontuacao da geracao: 0'   
ALIVE_TEXT = 'Individuos vivos: 0'      
GENERATION_TEXT = 'Geracoes passadas: 0'

DATA_FILE = './save'