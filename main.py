import curses
import sys

# Open the config file which is specified as the 2nd argument
config = open(sys.argv[1], 'rb')
size = int(config.read(10))
offset = size/2

screen = curses.initscr()

dim = screen.getmaxyx()
x_center = dim[1]/2
y_center = dim[0]/2

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
