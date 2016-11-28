import curses

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
                config.update({'size': 'FULLSCREEN'})
            else:
                config.update({'size': 
                    tuple(int(size.split("x")[i]) for i in range(2))
                })

    return config

f = open("config", 'rb')
config = parse(f)

screen = curses.initscr()
dim = screen.getmaxyx()

x_offset = config['size'][1]/2
y_offset = config['size'][0]/2
x_center = dim[1]/2
y_center = dim[0]/2

STATE_MENU = 0
STATE_GAME = 1
current_state = STATE_MENU

# Main game loop
while True:
    if current_state == STATE_MENU:
        screen.addstr(y_center+(y_offset+3), x_center-(x_offset),
                      "slithery")

    elif current_state == STATE_GAME: 
        if config['size'] != 'FULLSCREEN':
            # Draw borders
            screen.addstr(y_center+(y_offset+1), x_center-(x_offset-1),
                          "_"*(config['size'][1]-1))
            screen.addstr(y_center-(y_offset+1), x_center-(x_offset-1),
                          "_"*(config['size'][1]-1))
            for i in range(y_center-(y_offset-1), y_center+(y_offset+1)):
                screen.addstr(i, x_center-x_offset, "|")
                screen.addstr(i, x_center+x_offset, "|")
            
        screen.refresh()
        screen.getch()
        curses.endwin()
