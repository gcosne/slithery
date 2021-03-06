#!/usr/bin/python
import random
import curses
import sys
import math
import time
import logging

import values


class BaseItem(object):
    coord = None

    def spawn(self, board):
        while True:
            # Spawn at least a quarter into the board
            spawn_coord = (random.randint(0, values.HEIGHT-1),
                           random.randint(0, values.LENGTH-1))

            # Ensure there are no other items occupying the same spot
            if board.at(spawn_coord) is None:
                self.coord = spawn_coord
                return self


    def on_touch(self, game):
        # To be implemented by child classes
        pass


class Food(BaseItem):
    def on_touch(self, game):
        game.score += 1
        game.snake.grow(game.current_direction)
        game.screen.addstr(0, 0, 'Score: {}'.format(game.score))


class Snake(BaseItem):
    def __init__(self):
        super(Snake, self).__init__()
        self.coords = []


    def spawn(self, board):
        while True:
            spawn_coord = super(Snake, self).spawn(board).coord

            # A .0 is added at the back to prevent floating point truncation
            # math.ceil is used to better approximate the upper limit of x and y
            if spawn_coord[0] in range(int((1.0/4.0)*values.HEIGHT),
                                       int(math.ceil((3.0/4.0)*values.HEIGHT))+1) \
                and spawn_coord[1] in range(int((1.0/4.0)*values.LENGTH),
                                            int(math.ceil((3.0/4.0)*values.LENGTH))+1):
                self.coords.append(spawn_coord)
                break


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
    def __init__(self, screen):
        self.screen = screen
        self.grid = []

        for i in range(values.HEIGHT):
            row = []
            for j in range(values.LENGTH):
                row.append(None)
            self.grid.append(row)


    def at(self, coord):
        return self.grid[coord[0]][coord[1]]


    def within(self, coord):
        return coord[0] >= 0 and coord[0] < values.HEIGHT \
           and coord[1] >= 0 and coord[1] < values.LENGTH


    def draw(self):
        display_map = {Food: values.DISPLAY_FOOD,
                       Snake: values.DISPLAY_SNAKE,
                       type(None): values.DISPLAY_EMPTY}

        for index, row in enumerate(self.grid):
            self.screen.addstr(values.CORNERS['TOP_LEFT'][0]+index, values.CORNERS['TOP_LEFT'][1],
                               ''.join(list([display_map[item.__class__] for item in row])))


    def apply(self, items):
        def replace(item, coord):
            self.grid[coord[0]][coord[1]] = item

        for i in range(values.HEIGHT):
            for j in range(values.LENGTH):
                self.grid[i][j] = None

        for item in items:
            # Snake object stores multiple coordinates
            if isinstance(item, Snake):
                for i in item.coords:
                    replace(item, i)
            else:
                replace(item, item.coord)


class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.screen.nodelay(1)
        self.screen.clear()

        self.board = None
        self.snake = None
        self.items = []
        self.direction_map = {ord(values.PLAYER_KEYS[0][0]): values.DIRECTION_UP,
                              ord(values.PLAYER_KEYS[0][1]): values.DIRECTION_DOWN,
                              ord(values.PLAYER_KEYS[0][2]): values.DIRECTION_LEFT,
                              ord(values.PLAYER_KEYS[0][3]): values.DIRECTION_RIGHT}
        self.current_direction = random.randint(0, 3)
        self.score = 0


    def start(self):
        self.draw_borders()
        self.screen.addstr(0, 0, 'Score: 0')

        self.board = Board(self.screen)
        self.snake = Snake()
        self.snake.spawn(self.board)

        self.items.append(Food().spawn(self.board))

        while True:
            self.items.append(self.snake)
            self.board.apply(self.items)
            self.board.draw()
            self.screen.refresh()

            c = self.screen.getch()

            time.sleep(values.ITERATION_DELAY)
            if c == ord('q'):
                return False
            elif c in self.direction_map.keys():
                self.current_direction = self.direction_map[c]

            extrapolate = self.snake.extrapolate(self.current_direction)
            if self.board.within(extrapolate) and not isinstance(self.board.at(extrapolate), Snake):
                self.snake.move(self.current_direction)

                item = self.board.at(extrapolate)
                if isinstance(item, BaseItem):
                    item.on_touch(self)

                    # Remove the powerup that has already been collected
                    for i in self.items:
                        if isinstance(i, item.__class__) and i.coord == item.coord:
                            self.items.remove(i)

                            if isinstance(i, Food):
                                self.items.append(Food().spawn(self.board))
            else:
                return self.game_over()


    def game_over(self):
        self.screen.clear()
        self.screen.addstr(0, 0, 'Score: {}'.format(self.score))
        self.screen.addstr(1, 0, 'Press y to play again and n to quit')
        
        self.screen.nodelay(0)
        while True:
            c = self.screen.getch()

            if c == ord('y'):
                self.screen.nodelay(1)
                return True
            elif c == ord('n'):
                return False


    def draw_borders(self):
        # Draw sides
        for i in range(values.BOARD_EDGES['MIN_X']-1, values.BOARD_EDGES['MAX_X']):
            self.screen.addch(values.BOARD_EDGES['MIN_Y']-1, i, values.BORDERS['TOP'])
            self.screen.addch(values.BOARD_EDGES['MAX_Y'], i, values.BORDERS['BOTTOM'])

        for i in range(values.BOARD_EDGES['MIN_Y']-1, values.BOARD_EDGES['MAX_Y']):
            self.screen.addch(i, values.BOARD_EDGES['MIN_X']-1, values.BORDERS['LEFT'])
            self.screen.addch(i, values.BOARD_EDGES['MAX_X'], values.BORDERS['RIGHT'])

        # Draw corners
        self.screen.addch(values.BOARD_EDGES['MIN_Y']-1, values.BOARD_EDGES['MIN_X']-1,
                          values.BORDERS['TOP_LEFT'])
        self.screen.addch(values.BOARD_EDGES['MIN_Y']-1, values.BOARD_EDGES['MAX_X'],
                          values.BORDERS['TOP_RIGHT'])
        self.screen.addch(values.BOARD_EDGES['MAX_Y'], values.BOARD_EDGES['MIN_X']-1,
                          values.BORDERS['BOTTOM_LEFT'])
        self.screen.move(0, 0)
        self.screen.addch(values.BOARD_EDGES['MAX_Y'], values.BOARD_EDGES['MAX_X'],
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


    def populate_values(filename):
        def get_config_value(arg):
            return arg.split('=', 1)[1]

        for line in filename:
            line = line.strip('\n')

            if 'boardsize' in line:
                size = get_config_value(line)

                if size == 'MAX':
                    values.HEIGHT = values.SCREEN_DIMENSIONS[0]-4
                    values.LENGTH = values.SCREEN_DIMENSIONS[1]-4
                else:
                    size_split = tuple(int(size.split('x')[i]) for i in range(2))

                    if any(size_split[i]+2 >= values.SCREEN_DIMENSIONS[i] for i in range(2)):
                        terminate('Error: width and height must not be greater than the ' +
                                  'maximum dimensions')

                        if any(size_split[i] < 10 for i in range(2)):
                            terminate('Error: width and height must be both at least 10')

                    if any(size_split[i]%2 != 0 for i in range(2)):
                        terminate('Error: width and height must be even numbers')

                    values.LENGTH = size_split[0]
                    values.HEIGHT = size_split[1]

            if 'displaysnake' in line:
                display_snake = get_config_value(line)

                if len(display_snake) != 1:
                    terminate('Error: snake must be only 1 character')

                values.DISPLAY_SNAKE = display_snake

            if 'displayfood' in line:
                display_food = get_config_value(line)

                if len(display_food) != 1:
                    terminate('Error: food must be only 1 character')

                values.DISPLAY_FOOD = display_food

            if 'displayempty' in line:
                display_empty = get_config_value(line)

                if display_empty == 'SPACE':
                    values.DISPLAY_EMPTY = ' '
                else:
                    if len(display_empty) != 1:
                        terminate('Error: empty item must be only 1 character')

                    values.DISPLAY_EMPTY = display_empty

            if 'iterdelay' in line:
                iteration_delay_str = get_config_value(line)
                iteration_delay_float = float(iteration_delay_str)

                if iteration_delay_float < 0.025 or iteration_delay_float > 2:
                    terminate('Error: iteration delay must be between 0.025 and 2 seconds')

                values.ITERATION_DELAY = iteration_delay_float

            if 'player1keys' in line:
                player1_keys = get_config_value(line)
                player1_keys_split = tuple(player1_keys.split(',')[i] for i in range(4))

                if any(len(player1_keys_split[i]) != 1 for i in range(4)):
                    terminate('Error: movement keys must be only 1 character')

                values.PLAYER_KEYS = []
                values.PLAYER_KEYS.append(player1_keys_split)

            if 'quitkey' in line:
                quit_key = get_config_value(line)

                if len(quit_key) != 1:
                    terminate('Error: quit key must be only 1 character')

                values.QUIT_KEY = quit_key


    config = None
    config_file = None
    try:
        # slithery.conf is the default file to read from, other files can be specified as
        # the first argument to `python main.py`
        config_file = open(['slithery.conf' if len(sys.argv) == 1 else sys.argv[1]][0], 'rb')
    except IOError:
        terminate('Error: configuration file does not exist in current directory')
    else:
        populate_values(config_file)

        values.SCREEN_X_CENTER = values.SCREEN_DIMENSIONS[1]/2
        values.SCREEN_Y_CENTER = values.SCREEN_DIMENSIONS[0]/2

        values.BORDERS = {'TOP': curses.ACS_HLINE,
                          'BOTTOM': curses.ACS_HLINE,
                          'LEFT': curses.ACS_VLINE,
                          'RIGHT': curses.ACS_VLINE,
                          'TOP_LEFT': curses.ACS_ULCORNER,
                          'TOP_RIGHT': curses.ACS_URCORNER,
                          'BOTTOM_LEFT': curses.ACS_LLCORNER,
                          'BOTTOM_RIGHT': curses.ACS_LRCORNER}

        values.BOARD_EDGES = {'MIN_Y': (values.SCREEN_DIMENSIONS[0]-values.HEIGHT)/2,
                              'MAX_Y': values.SCREEN_DIMENSIONS[0]
                                       -(values.SCREEN_DIMENSIONS[0]-values.HEIGHT)/2,
                              'MIN_X': (values.SCREEN_DIMENSIONS[1]-values.LENGTH)/2,
                              'MAX_X': values.SCREEN_DIMENSIONS[1]
                                       -(values.SCREEN_DIMENSIONS[1]-values.LENGTH)/2}

        values.CORNERS = {'TOP_LEFT': (values.BOARD_EDGES['MIN_Y'], values.BOARD_EDGES['MIN_X']),
                          'TOP_RIGHT': (values.BOARD_EDGES['MIN_Y'], values.BOARD_EDGES['MAX_X']),
                          'BOTTOM_LEFT': (values.BOARD_EDGES['MAX_Y'], values.BOARD_EDGES['MIN_X']),
                          'BOTTOM_RIGHT': (values.BOARD_EDGES['MAX_Y'], values.BOARD_EDGES['MAX_X'])}

        logging.basicConfig(filename='slithery.log', level=logging.DEBUG)

    # Main game loop
    while True:
        game = Game(screen)
        play_again = game.start()

        if not play_again:
            terminate()
