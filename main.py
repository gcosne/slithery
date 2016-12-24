#!/usr/bin/python
import random
import curses
import sys

import values


class BaseItem(object):
    def get_spawn(self, board):
        while True:
            # Spawn at least a quarter into the board
            spawn_coords = (random.randint((1/4)*values.HEIGHT, (3/4)*values.HEIGHT),
                            random.randint((1/4)*values.LENGTH, (3/4)*values.LENGTH))

            # Ensure there are no other powerups occupying the same spot
            if board.at(spawn_coords) == '':
                return spawn_coords


class Snake(BaseItem):
    coords = []

    def __init__(self):
        super(Snake, self).__init__()


    def get_spawn(self, board):
        spawn_coords = super(Snake, self).get_spawn(board)
        self.coords.append(spawn_coords)
        return spawn_coords


    def extrapolate(self, direction):
        extrapolation_map = {values.DIRECTION_UP: (-1, 0),
                             values.DIRECTION_DOWN: (1, 0),
                             values.DIRECTION_LEFT: (0, -1),
                             values.DIRECTION_RIGHT: (0, 1)}
        return (self.coords[0][i] + extrapolation_map[direction][i] for i in range(2))


    def move(self, direction):
        self.coords.insert(0, self.extrapolate(direction))
        del self.coords[len(self.coords)-1]


    def grow(self, direction):
        spawn_map = {values.DIRECTION_UP: (1, 0),
                     values.DIRECTION_DOWN: (-1, 0),
                     values.DIRECTION_LEFT: (0, -1),
                     values.DIRECTION_RIGHT: (0, 1)}
        self.coords.append(spawn_map[direction])


class Board(object):
    grid = []

    def __init__(self, screen):
        self.screen = screen

        for i in range(values.HEIGHT):
            row = []
            for j in range(values.LENGTH):
                row.append('')
            self.grid.append(row)


    def at(self, coords):
        return self.grid[coords[0]][coords[1]]


    def within(self, coords):
        return coords[0] < 0 or coords[0] >= values.HEIGHT \
            or coords[1] < 0 or coords[1] >= values.LENGTH


    def draw(self):
        for index, row in enumerate(self.grid):
            self.screen.addstr(values.CORNERS['top_left'][0]+index, values.CORNERS['top_left'][1],
                               ''.join(row))


    def apply(self, items):
        def replace(item, coords):
            self.grid[coords[0]][coords[1]] = item

        item_map = {values.ITEM_FOOD: config['snake'],
                    values.ITEM_SNAKE: config['food']}

        self.__clear()
        for key, value in items.iteritems():
            for i in value:
                replace(item_map[key], i)


    def __clear(self):
        for i in range(values.HEIGHT):
            for j in range(values.LENGTH):
                self.grid[i][j] = ''


class Game(object):
    current_direction = None


    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.board = None


    def start(self):
        self.board = Board(self.screen)


    def draw_borders(self):
        self.screen.addstr(values.CORNERS['top_left'][0]-1, values.CORNERS['top_left'][1],
                           values.CORNERS['top']*values.LENGTH)
        self.screen.addstr(values.CORNERS['bottom_left'][0], values.CORNERS['bottom_left'][1],
                           values.CORNERS['bottom']*values.LENGTH)

        for i in range(values.CORNERS['top_left'][0], values.CORNERS['bottom_left'][0]):
            self.screen.addstr(i, values.CORNERS['top_left'][1]-1, values.CORNERS['left'])
            self.screen.addstr(i, values.CORNERS['top_right'][1]+1, values.CORNERS['right'])


if __name__ == '__main__':
    screen = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    values.SCREEN_DIMENSIONS = screen.getmaxyx()


    def terminate(*args):
        curses.endwin()
        curses.curs_set(1)

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
                    value.update({'size': values.SCREEN_DIMENSIONS})
                else:
                    size_split = tuple(int(size.split('x')[i]) for i in range(2))

                    if any(size_split[i] > values.SCREEN_DIMENSIONS[i] for i in range(2)):
                        terminate("Error: width and HEIGHT must not be greater than the " +
                                  "maximum dimensions")

                    if any(size_split[i] < 10 for i in range(2)):
                        terminate("Error: width and HEIGHT must be both at least 10")

                    if any(size_split[i]%2 != 0 for i in range(2)):
                        terminate("Error: width and HEIGHT must be even numbers")

                    value.update({'size': size_split})

            if 'borders' in line:
                borders = get_config_value(line)
                borders_split = tuple(borders.split(',')[i] for i in range(4))

                if any(len(borders_split[i]) != 1 for i in range(4)):
                    terminate("Error: each border must be only 1 character")

                # Left, right, top, bottom
                value.update({'borders': borders_split})

            if 'snake' in line:
                snake_char = get_config_value(line)

                if len(snake_char) != 1:
                    terminate("Error: snake must be only 1 character")

                value.update({'snake': snake_char})

            if 'food' in line:
                food_char = get_config_value(line)

                if len(food_char) != 1:
                    terminate("Error: food must be only 1 character")

                value.update({'food': food_char})

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
        values.LENGTH = config['size'][1]
        values.HEIGHT = config['size'][0]
        values.X_CENTER = values.SCREEN_DIMENSIONS[1]/2
        values.Y_CENTER = values.SCREEN_DIMENSIONS[0]/2

        values.BORDERS = {'top': config['borders'][2],
                          'bottom': config['borders'][3],
                          'left': config['borders'][0],
                          'right': config['borders'][1]}

        values.CORNERS = {'top_left': (values.Y_CENTER-values.HEIGHT/2+2,
                                       values.X_CENTER-values.LENGTH/2+1),
                          'top_right': (values.Y_CENTER-values.HEIGHT/2+2,
                                        values.X_CENTER-values.LENGTH/2),
                          'bottom_left': (values.Y_CENTER+values.HEIGHT/2+2,
                                          values.X_CENTER-values.LENGTH/2+1),
                          'bottom_right': (values.Y_CENTER+values.HEIGHT/2+2,
                                           values.X_CENTER+values.LENGTH/2)}


    # Main game loop
    while True:
        game = Game(config, screen)
        play_again = game.start()

        if not play_again:
            break
