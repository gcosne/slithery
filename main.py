import curses
import sys
import os

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
dim = screen.getmaxyx()

def exit(*args):
    curses.endwin()
    curses.curs_set(1)
    
    # Reserved for error messages
    if len(args) != 0:
        print args[0]

    sys.exit()

def parse(file):
    def get_config_value(str):
        # Gets the text after '='
        return str.split('=', 1)[1]

    config = {}
    for line in file:
        line = line.strip('\n')

        if 'size' in line:
            size = get_config_value(line)

            if size == 'FULLSCREEN':
                config.update({'size': dim})
            else:
                size_split = tuple(int(size.split('x')[i]) for i in range(2))

                if any(size_split[i] > dim[i] for i in range(2)): 
                    exit("Error: width and height must not be greater than the maximum dimensions")

                if any(size_split[i] < 6 for i in range(2)):
                    exit("Error: width and height must be both at least 6")

                if any(size_split[i]%2 != 0 for i in range(2)):
                    exit("Error: width and height must be even numbers")

                config.update({'size': size_split})

        if 'borders' in line:
            borders = get_config_value(line)
            config.update({'borders': 
                # Left, right, top, bottom
                tuple(borders.split(",")[i] for i in range(4))               
            })

    return config

f = open('config', 'rb')
config = parse(f)

# curses coordinates are in the format {y, x}
x = config['size'][1]
y = config['size'][0]
x_center = dim[1]/2
y_center = dim[0]/2

# Top left, top right, bottom left, bottom right
board_coords = {'TOP_LEFT': (y_center-y/2+2, x_center-x/2+1),
        'TOP_RIGHT': (y_center-y/2+2, x_center+x/2),
        'BOTTOM_LEFT': (y_center+y/2+2, x_center-x/2+1),
        'BOTTOM_RIGHT': (y_center+y/2+2, x_center+x/2)}

STATE_MENU = 0
STATE_GAME = 1
current_state = STATE_MENU

MENU_SINGLEPLAYER = 0
MENU_MULTIPLAYER = 1
current_menu = MENU_SINGLEPLAYER 
c = None

board = []
ITEM_EMPTY = 0
ITEM_SNAKE = 1
ITEM_FOOD = 2

def init_singleplayer_board():
    for i in range(y):
        row = []
        for j in range(x):
            row.append(ITEM_EMPTY)
        board.append(row)

def merge_row_to_string(row):
    items_text = {ITEM_EMPTY: '^',
            ITEM_SNAKE: 'O',
            ITEM_FOOD: '*'}
    string = ""

    for i in row:
        string += items_text[i]
    return string

def draw_board():
    for index, row in enumerate(board):
        print index
        print len(row)
        screen.addstr(board_coords['TOP_LEFT'][0]+index, board_coords['TOP_LEFT'][1], merge_row_to_string(row))

def draw_menu_items():
    screen.addstr(y_center-2, x_center-4, 'slithery', curses.A_BOLD)
    screen.addstr(y_center, x_center-4, '1-player',
            curses.A_BOLD if current_menu == MENU_SINGLEPLAYER else curses.A_NORMAL)
    screen.addstr(y_center+2, x_center-6, 'Multi-player', 
            curses.A_BOLD if current_menu == MENU_MULTIPLAYER else curses.A_NORMAL)

def draw_borders():
    screen.addstr(board_coords['TOP_LEFT'][0]-1, board_coords['TOP_LEFT'][1], config['borders'][2]*x)
    screen.addstr(board_coords['BOTTOM_LEFT'][0], board_coords['BOTTOM_LEFT'][1], config['borders'][3]*x)
    for i in range(board_coords['TOP_LEFT'][0], board_coords['BOTTOM_LEFT'][0]):
        screen.addstr(i, board_coords['TOP_LEFT'][1]-1, config['borders'][0])
        screen.addstr(i, board_coords['TOP_RIGHT'][1]+1, config['borders'][1])

# Main game loop
while True:
    if current_state == STATE_MENU:
        draw_menu_items() 
    elif current_state == STATE_GAME: 
        if config['size'] != dim:
            draw_borders()

            init_singleplayer_board()
            draw_board()

    screen.refresh()

    # Check for keyboard input
    c = screen.getch()

    if c == ord('d') and current_menu < 1:
        current_menu += 1
    elif c == ord('w') and current_menu > 0:
        current_menu -= 1
    
    if c == ord('\n'):
        if current_menu == MENU_SINGLEPLAYER:
            screen.clear()
            current_state = STATE_GAME

    if c == ord('q'):
        exit()
