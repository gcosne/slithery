#!/usr/bin/python

import curses
import sys
import random

import values
from Game import Game

screen = curses.initscr()
curses.curs_set(0)
curses.noecho()
screen_dimensions = screen.getmaxyx()


def terminate(*args):
    # Reserved for error messages
    if len(args) != 0:
        print args[0]

    sys.exit()


def parse(filename):
    def get_config_value(arg):
        return arg.split('=', 1)[1]

    value = {}
    for line in filename:
        line = line.strip('\n')

        if 'size' in line:
            size = get_config_value(line)

            if size == 'FULLSCREEN':
                value.update({'size': dim})
            else:
                size_split = tuple(int(size.split('x')[i]) for i in range(2))

                if any(size_split[i] > dimensions[i] for i in range(2)):
                    terminate("Error: width and height must not be greater than the " +
                              "maximum dimensions")

                if any(size_split[i] < 10 for i in range(2)):
                    terminate("Error: width and height must be both at least 10")

                if any(size_split[i]%2 != 0 for i in range(2)):
                    terminate("Error: width and height must be even numbers")

                value.update({'size': size_split})

        if 'borders' in line:
            borders = get_config_value(line)
            borders_split = tuple(borders.split(',')[i] for i in range(4))

            if any(len(borders_split[i]) != 1 for i in range(4)):
                terminate("Error: each border must be only 1 character")

            # Left, right, top, bottom
            value.update({'borders': borders_split}) 

    return value

config = None
config_file = None
try:
    # slithery.conf is the default file to read from, other files can be specified as
    # the first argument to `python main.py`
    config_file = open(['slithery.conf' if len(sys.argv) == 1 else sys.argv[1]][0], 'rb')
except IOError:
    terminate("Error: configuration file does not exist in current directory")
else:
    config = parse(config_file)

    # curses coordinates are in the format (y, x)
    values.SCREEN_DIMENSIONS = screen_dimensions
    values.LENGTH = config['size'][1]
    values.HEIGHT = config['size'][0]
    values.X_CENTER = dimensions[1]/2
    values.Y_CENTER = dimensions[0]/2

    values.BORDERS = {'TOP': config['borders'][2],
                      'BOTTOM': config['borders'][3],
                      'LEFT': config['borders'][0],
                      'RIGHT': config['borders'][1]}

    values.CORNERS = {'TOP_LEFT': (values.y_center-values.height/2+2, values.x_center-values.length/2+1),
                      'TOP_RIGHT': (values.y_center-values.height/2+2, values.x_center-values.length/2),
                      'BOTTOM_LEFT': (values.y_center+values.height/2+2, values.x_center-values.length/2+1),
                      'BOTTOM_RIGHT': (values.y_center+values.height/2+2, values.x_center+values.length/2)}


# Main game loop
while True:
    game = Game(config, screen)
    play_again = game.start()

    if not play_again:
        break
