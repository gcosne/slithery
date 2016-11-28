import curses
import sys

# Open the configuration file which is specified as the 2nd argument
f = open('config', 'rb')
config = parse(f)

screen = curses.initscr()

dim = screen.getmaxyx()
x_center = dim[1]/2
y_center = dim[0]/2

# Draw borders
screen.addstr(y_center+(offset+1), x_center-(offset-1),
              "_________")
screen.addstr(y_center-(offset+1), x_center-(offset-1),
              "_________")
for i in range(y_center-(offset-1), y_center+(offset+1)):
    screen.addstr(i, x_center-offset, "|")
    screen.addstr(i, x_center+offset, "|")
screen.refresh()
screen.getch()
curses.endwin()

def parse(file):
    def get_config_value(val):
        return val.split('=', 1)[1]

    config_data = {}
    for line in file:
        if 'SIZE' in line:
            size = get_config_value(line)
            if size == 'FULLSCREEN':
                config_data.update({'size': dim})
            else:
                config_data.update({'size': 
                    [size.split("x")[i] for i in range(1)]
                })
