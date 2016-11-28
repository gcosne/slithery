import curses

screen = curses.initscr()
dim = screen.getmaxyx()

def parse(file):
    def get_config_value(str):
        # Gets the text after '='
        return str.split('=', 1)[1]

    config = {}
    for line in file:
        line = line.strip('\n')
        if 'SIZE' in line:
            size = get_config_value(line)
            if size == 'FULLSCREEN':
                config.update({'size': dim})
            else:
                config.update({'size': 
                    tuple(int(size.split("x")[i]) for i in range(2))
                })

    return config

f = open('config', 'rb')
config = parse(f)

x = config['size'][1]
y = config['size'][0]
x_center = dim[1]/2
y_center = dim[0]/2

STATE_MENU = 0
STATE_GAME = 1
current_state = STATE_MENU
menu_y = 0

c = None

# Main game loop
while True:
    if current_state == STATE_MENU:
        screen.addstr(y_center-3, x_center-4, 'slithery', curses.A_BOLD)
        screen.addstr(y_center-1, x_center-4, '1-player', curses.A_BOLD if menu_y == 0 else curses.A_NORMAL)
        screen.addstr(y_center+1, x_center-6, 'Multi-player', curses.A_BOLD if menu_y == 1 else curses.A_NORMAL)
        screen.addstr(y_center+3, x_center-2, 'Quit', curses.A_BOLD if menu_y == 2 else curses.A_NORMAL)
        
    elif current_state == STATE_GAME: 
        if config['size'] != dim:
            # Draw borders
            screen.addstr(y_center+(y/2+1), x_center-(x/2-1), '-'*(x/2-1))
            screen.addstr(y_center-(y/2+1), x_center-(x/2-1), '_'*(x/2-1))
            for i in range(y_center-(y/2-1), y_center+(y/2+1)):
                screen.addstr(i, x_center-x_offset, '|')
                screen.addstr(i, x_center+x_offset, '|')

    screen.refresh()    
    c = screen.getch()

    if c == ord('d') and menu_y < 2:
        menu_y += 1
    elif c == ord('w') and menu_y > 0:
        menu_y -= 1

curses.endwin()
