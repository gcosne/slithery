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

STATE_MENU = 0
STATE_GAME = 1
current_state = STATE_MENU

MENU_SINGLEPLAYER = 0
MENU_MULTIPLAYER = 1
menu_y = MENU_SINGLEPLAYER

c = None

def draw_menu_items():
    screen.addstr(y_center-2, x_center-4, 'slithery', curses.A_BOLD)
    screen.addstr(y_center, x_center-4, '1-player', curses.A_BOLD if menu_y == MENU_SINGLEPLAYER else curses.A_NORMAL)
    screen.addstr(y_center+2, x_center-6, 'Multi-player', curses.A_BOLD if menu_y == MENU_MULTIPLAYER else curses.A_NORMAL)

def draw_borders():
    screen.addstr(y_center-(y/2), x_center-(x/2-1), config['borders'][2]*(x-1))
    screen.addstr(y_center+(y/2+1), x_center-(x/2-1), config['borders'][3]*(x-1))
    for i in range(y_center-(y/2-1), y_center+(y/2+1)):
        screen.addstr(i, x_center-x/2, config['borders'][0])
        screen.addstr(i, x_center+x/2, config['borders'][1])

# Main game loop
while True:
    if current_state == STATE_MENU:
        draw_menu_items() 
    elif current_state == STATE_GAME: 
        if config['size'] != dim:
            draw_borders()

    screen.refresh()

    # Check for keyboard input
    c = screen.getch()

    if c == ord('d') and menu_y < 1:
        menu_y += 1
    elif c == ord('w') and menu_y > 0:
        menu_y -= 1
    
    if c == ord('\n'):
        if menu_y == MENU_SINGLEPLAYER:
            screen.clear()
            current_state = STATE_GAME

    if c == ord('q'):
        exit()
