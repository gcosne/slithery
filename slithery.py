#!/usr/bin/python
import random
import curses
import sys

import values


class BaseItem:
    def __init__(self):
        pass

    
    def get_spawn(self, board):
        while True:
            # Spawn at least a quarter into the board
            spawn_coords = (random.randint((1/4)*values.HEIGHT, (3/4)*values.HEIGHT), 
                            random.randint((1/4)*values.LENGTH, (3/4)*values.LENGTH))

            # Ensure there are no other powerups occupying the same spot
            if board.at(spawn_coords) == '':
                return spawn_coords


class Snake(BaseItem):
    coords = {}

    def __init__(self, board):
        pass


    def get_spawn(self, board):
            # Spawn at least a quarter into the board
            spawn_coords = (random.randint((1/4)*values.HEIGHT, (3/4)*values.HEIGHT), 
                            random.randint((1/4)*values.LENGTH, (3/4)*values.LENGTH))
            
            # Ensure there are no other powerups occupying the same spot
            if board.at(spawn_coords) == '':
                self.coords.update({'head': spawn_coords})
                return spawn_coords


    def extrapolate(self, direction):
        extrapolation_map = {values.DIRECTION_UP: (-1, 0),
                             values.DIRECTON_DOWN: (1, 0),
                             values.DIRECTION_LEFT: (0, -1),
                             values.DIRECTION_RIGHT: (0, 1)}
        
        return (head[i] + extrapolation_map[direction][i] for i in range(2))


class Board:
    grid = []

    def __init__(self, screen, config):
        self.screen = screen

        for i in range(values.HEIGHT):
            row = []
            for j in range(values.LENGTH):
                row.append('')
            self.grid.append(row)

    
    def at(self, coords):
        return grid[coords[0]][coords[1]]

    
    def draw(self):
        for index, row in enumerate(self.grid):
            self.screen.addstr(values.CORNERS['top_left'][0]+index, values.CORNERS['top_left'][1],
                               ''.join(row))


    def apply(self, items):
        def replace(item, coords):
            board[coords[0]][coords[1]] = item

        item_map = {values.ITEM_FOOD: config['snake'],
                    values.ITEM_SNAKE: config['food']}

        __clear()
        for key, value in items.iteritems():
            for i in value:
                replace(item_map[key], i)


    def __clear(self):
        for i in range(values.HEIGHT):
            for j in range(values.LENGTH):
                board[i][j] = ''


class Game:
    current_direction = None


    def __init__(self, config, screen):
        self.config = config
        self.screen = screen


    def start():
        self.board = Board(self.screen, self.config)


    def draw_borders():
        self.screen.addstr(values.CORNERS['top_left'][0]-1, values.CORNERS['top_left'][1], values.CORNERS['top']*x)
        self.screen.addstr(values.CORNERS['bottom_left'][0], values.CORNERS['bottom_left'][1], values.CORNERS['bottom']*x)
        for i in range(values.CORNERS['top_left'][0], values.CORNERS['bottom_left'][0]):
            self.screen.addstr(i, values.CORNERS['top_left'][1]-1, values.CORNERS['left']) 
            self.screen.addstr(i, values.CORNERS['top_right'][1]+1, values.CORNERS['right'])


    def iteration(char):
        direction_keymap = {'w': DIRECTION_UP,
                            's': DIRECTION_DOWN,
                            'a': DIRECTION_left,
                            'd': DIRECTION_right}

        # The x and y values to move the snake's head
        coord_diff = {DIRECTION_UP: (-1, 0),
                             DIRECTION_DOWN: (1, 0),
                             DIRECTION_left: (0, -1),
                             DIRECTION_right: (0, 1)}

        char_lower = str.lower(char)
        current_direction = direction_keymap[char]
        new_head = coord_add(snake_head, coord_diff[current_direction])

        # Out of borders
        if new_head[0] < self.corners['top_left'][0] or new_head[0] > corners['bottom_left'][0] \
                or new_head[1] < self.corners['top_left'][1] or new_head[0] > corners['top_right'][1]:
            return 1
        else:
            snake_head = new_head

            if snake_head == 0:
                pass


if __name__ == '__main__':
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

            if 'snake' in line:
                snake_char = get_config_value(line)

                if len(snake_char) != 1:
                    terminate("Error: snake must be only 1 character")

                values.update({'snake': snake_char})

            if 'food' in line:
                food_char = get_config_value(line)
                
                if len(food_char) != 1:
                    terminate("Error: food must be only 1 character")

                values.update({'food': food_char})

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

        values.BORDERS = {'top': config['borders'][2],
                          'bottom': config['borders'][3],
                          'left': config['borders'][0],
                          'right': config['borders'][1]}

        values.CORNERS = {'top_left': (values.y_center-values.height/2+2, values.x_center-values.length/2+1),
                          'top_right': (values.y_center-values.height/2+2, values.x_center-values.length/2),
                          'bottom_left': (values.y_center+values.height/2+2, values.x_center-values.length/2+1),
                          'bottom_right': (values.y_center+values.height/2+2, values.x_center+values.length/2)}


    # Main game loop
    while True:
        game = Game(config, screen)
        play_again = game.start()

        if not play_again:
            break
