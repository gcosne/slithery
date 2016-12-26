#!/usr/bin/python
import random
import curses
import sys
import math
import time

import values


class BaseItem(object):
    def spawn(self, board):
        while True:
            # Spawn at least a quarter into the board
            spawn_coord = (random.randint(0, values.HEIGHT-1),
                           random.randint(0, values.LENGTH-1))

            # Ensure there are no other powerups occupying the same spot
            if board.at(spawn_coord) == values.ITEM_EMPTY:
                return spawn_coord


class Snake(BaseItem):
    coords = []

    def __init__(self):
        super(Snake, self).__init__()


    def spawn(self, board):
        while True:
            spawn_coord = super(Snake, self).spawn(board)

            # A .0 is added at the back to prevent floating point truncation
            # math.ceil is used to better approximate the upper limit of x and y
            if spawn_coord[0] in range(int((1.0/4.0)*values.HEIGHT),
                                       int(math.ceil((3.0/4.0)*values.HEIGHT))+1) \
               and spawn_coord[1] in range(int((1.0/4.0)*values.LENGTH),
                                           int(math.ceil((3.0/4.0)*values.LENGTH))+1):
                self.coords.append(spawn_coord)
                return spawn_coord


    def extrapolate(self, direction):
        extrapolation_map = {values.DIRECTION_UP: (-1, 0),
                             values.DIRECTION_DOWN: (1, 0),
                             values.DIRECTION_LEFT: (0, -1),
                             values.DIRECTION_RIGHT: (0, 1)}
        return list(self.coords[0][i] + extrapolation_map[direction][i] for i in range(2))


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
                row.append(values.ITEM_EMPTY)
            self.grid.append(row)


    def at(self, coord):
        return self.grid[coord[0]][coord[1]]


    def within(self, coord):
        return coord[0] < 0 or coord[0] >= values.HEIGHT \
            or coord[1] < 0 or coord[1] >= values.LENGTH


    def draw(self):
        item_map = {values.ITEM_FOOD: values.DISPLAY_FOOD,
                    values.ITEM_SNAKE: values.DISPLAY_SNAKE,
                    values.ITEM_EMPTY: values.DISPLAY_EMPTY}

        for index, row in enumerate(self.grid):
            self.screen.addstr(values.CORNERS['TOP_LEFT'][0]+index, values.CORNERS['TOP_LEFT'][1],
                               ' '.join(list([item_map[item] for item in row])))


    def apply(self, items):
        def replace(item, coord):
            self.grid[coord[0]][coord[1]] = item

        self.__clear()
        for key, coords in items.iteritems():
            for coord in coords:
                replace(key, coord)


    def __clear(self):
        for i in range(values.HEIGHT):
            for j in range(values.LENGTH):
                self.grid[i][j] = values.ITEM_EMPTY


class Game(object):
    def __init__(self, config, screen):
        self.config = config
        self.screen = screen
        self.board = None
        self.snake = None
        self.direction_map = {ord(values.PLAYER_KEYS[0][0]): values.DIRECTION_UP,
                              ord(values.PLAYER_KEYS[0][1]): values.DIRECTION_DOWN,
                              ord(values.PLAYER_KEYS[0][2]): values.DIRECTION_LEFT,
                              ord(values.PLAYER_KEYS[0][3]): values.DIRECTION_RIGHT}
        self.current_direction = random.randint(0, 3)


    def start(self):
        self.draw_borders()
        self.board = Board(self.screen)

        self.snake = Snake()
        self.snake.spawn()

        while True:
            self.board.apply({values.ITEM_SNAKE: self.snake.coords})
            self.board.draw()
            self.screen.refresh()

            c = self.screen.getch()
            if c == ord('q'):
                return False
            elif c in self.direction_map.keys():
                self.current_direction = self.direction_map[c]

            if self.board.within(self.snake.extrapolate(self.current_direction)):
                self.snake.move(self.current_direction)
            else:
                continue
                #return False

            time.sleep(0.5)


    def draw_borders(self):
        # Draw sides
        for i in range(values.CORNERS['TOP_LEFT'][1], values.CORNERS['TOP_RIGHT'][1]+1):
            self.screen.addch(values.CORNERS['TOP_LEFT'][0]-1, i, values.BORDERS['TOP'])
            self.screen.addch(values.CORNERS['BOTTOM_LEFT'][0]+1, i, values.BORDERS['BOTTOM'])

        for i in range(values.CORNERS['TOP_LEFT'][0], values.CORNERS['BOTTOM_LEFT'][0]+1):
            self.screen.addch(i, values.CORNERS['TOP_LEFT'][1]-1, values.BORDERS['LEFT'])
            self.screen.addch(i, values.CORNERS['TOP_RIGHT'][1]+1, values.BORDERS['RIGHT'])

        # Draw corners
        self.screen.addch(values.CORNERS['TOP_LEFT'][0]-1, values.CORNERS['TOP_LEFT'][1]-1,
                          values.BORDERS['TOP_LEFT'])
        self.screen.addch(values.CORNERS['TOP_LEFT'][0]-1, values.CORNERS['TOP_RIGHT'][1]+1,
                          values.BORDERS['TOP_RIGHT'])
        self.screen.addch(values.CORNERS['BOTTOM_LEFT'][0]+1, values.CORNERS['BOTTOM_LEFT'][1]-1,
                          values.BORDERS['BOTTOM_LEFT'])
        self.screen.addch(values.CORNERS['BOTTOM_RIGHT'][0]+1, values.CORNERS['BOTTOM_RIGHT'][1]+1,
                          values.BORDERS['BOTTOM_RIGHT'])


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
                        terminate('Error: width and HEIGHT must not be greater than the ' +
                                  'maximum dimensions')

                    if any(size_split[i] < 10 for i in range(2)):
                        terminate('Error: width and HEIGHT must be both at least 10')

                    if any(size_split[i]%2 != 0 for i in range(2)):
                        terminate('Error: width and HEIGHT must be even numbers')

                    value.update({'size': size_split})

            if 'snake' in line:
                display_snake = get_config_value(line)

                if len(display_snake) != 1:
                    terminate('Error: snake must be only 1 character')

                value.update({'snake': display_snake})

            if 'food' in line:
                display_food = get_config_value(line)

                if len(display_food) != 1:
                    terminate('Error: food must be only 1 character')

                value.update({'food': display_food})

            if 'player1_keys' in line:
                player1_keys = get_config_value(line)
                player1_keys_split = tuple(player1_keys.split(',')[i] for i in range(4))

                if any(len(player1_keys_split[i]) != 1 for i in range(4)):
                    terminate('Error: movement keys must be only 1 character')

                value.update({'player1_keys': player1_keys_split})

            # TODO: Do the same for other players

        return value


    config = None
    config_file = None
    try:
        # slithery.conf is the default file to read from, other files can be specified as
        # the first argument to `python main.py`
        config_file = open(['slithery.conf' if len(sys.argv) == 1 else sys.argv[1]][0], 'rb')
    except IOError:
        terminate('Error: configuration file does not exist in current directory')
    else:
        config = parse(config_file)

        # curses coordinates are in the format (y, x)
        values.LENGTH = config['size'][1]
        values.HEIGHT = config['size'][0]
        values.X_CENTER = values.SCREEN_DIMENSIONS[1]/2
        values.Y_CENTER = values.SCREEN_DIMENSIONS[0]/2

        values.BORDERS = {'TOP': curses.ACS_HLINE,
                          'BOTTOM': curses.ACS_HLINE,
                          'LEFT': curses.ACS_VLINE,
                          'RIGHT': curses.ACS_VLINE,
                          'TOP_LEFT': curses.ACS_ULCORNER,
                          'TOP_RIGHT': curses.ACS_URCORNER,
                          'BOTTOM_LEFT': curses.ACS_LLCORNER,
                          'BOTTOM_RIGHT': curses.ACS_LRCORNER}

        values.CORNERS = {'TOP_LEFT': (values.Y_CENTER-values.HEIGHT/2+2,
                                       values.X_CENTER-values.LENGTH/2+1),
                          'TOP_RIGHT': (values.Y_CENTER-values.HEIGHT/2+2,
                                        values.X_CENTER+values.LENGTH/2),
                          'BOTTOM_LEFT': (values.Y_CENTER+values.HEIGHT/2+2,
                                          values.X_CENTER-values.LENGTH/2+1),
                          'BOTTOM_RIGHT': (values.Y_CENTER+values.HEIGHT/2+2,
                                           values.X_CENTER+values.LENGTH/2)}

        values.DISPLAY_SNAKE = config['snake']
        values.DISPLAY_FOOD = config['food']

        values.PLAYER_KEYS.append(config['player1_keys'])


    # Main game loop
    while True:
        game = Game(config, screen)
        play_again = game.start()

        if not play_again:
            terminate()
