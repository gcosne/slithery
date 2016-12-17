#!/usr/bin/python

import curses

import values
from Board import Board

class Game:
    current_direction = None


    def __init__(self, config, screen):
        self.config = config
        self.screen = screen

        self.dimensions = self.screen.getmaxyx()

        # curses coordinates are in the format {y, x}
        self.length = self.config['size'][0]
        self.height = self.config['size'][0]
        self.x_center = self.dimensions[1]/2
        self.y_center = self.dimensions[0]/2

        self.borders = {'TOP': self.config['borders'][2],
                        'BOTTOM': self.config['borders'][3],
                        'LEFT': self.config['borders'][0],
                        'RIGHT': self.config['borders'][1]}

        self.corners = {'TOP_LEFT': (self.y_center-self.height/2+2, self.x_center-self.length/2+1),
                        'TOP_RIGHT': (self.y_center-self.height/2+2, self.x_center+self.length/2),
                        'BOTTOM_LEFT': (self.y_center+self.height/2+2, self.x_center-self.length/2+1),
                        'BOTTOM_RIGHT': (self.y_center+self.height/2+2, self.x_center+self.length/2)}
    

    def start():
        self.board = Board(self.length, self.height, self.screen, self.corners)


    def draw_borders():
        self.screen.addstr(self.corners['TOP_LEFT'][0]-1, self.corners['TOP_LEFT'][1], self.borders['TOP']*x)
        self.screen.addstr(self.corners['BOTTOM_LEFT'][0], self.corners['BOTTOM_LEFT'][1], self.borders['BOTTOM']*x)
        for i in range(self.corners['TOP_LEFT'][0], self.corners['BOTTOM_LEFT'][0]):
            self.screen.addstr(i, self.corners['TOP_LEFT'][1]-1, self.borders['LEFT']) 
            self.screen.addstr(i, self.corners['TOP_RIGHT'][1]+1, self.borders['RIGHT'])


    def merge_row_to_string(row):
        items_text = {ITEM_EMPTY: '^',
                      ITEM_SNAKE_HEAD: 'O',
                      ITEM_SNAKE_BODY: 'O',
                      ITEM_SNAKE_TAIL: 'O',
                      ITEM_FOOD: '*'}
        string = ""

        for i in row:
            string += items_text[i]
        return string


    def iteration(char):
        direction_keymap = {'w': DIRECTION_UP,
                            's': DIRECTION_DOWN,
                            'a': DIRECTION_LEFT,
                            'd': DIRECTION_RIGHT}

        # The x and y values to move the snake's head
        coord_diff = {DIRECTION_UP: (-1, 0),
                             DIRECTION_DOWN: (1, 0),
                             DIRECTION_LEFT: (0, -1),
                             DIRECTION_RIGHT: (0, 1)}

        char_lower = str.lower(char)
        current_direction = direction_keymap[char]
        new_head = coord_add(snake_head, coord_diff[current_direction])

        # Out of borders
        if new_head[0] < self.corners['TOP_LEFT'][0] or new_head[0] > corners['BOTTOM_LEFT'][0] \
                or new_head[1] < self.corners['TOP_LEFT'][1] or new_head[0] > corners['TOP_RIGHT'][1]:
            return 1
        else:
            snake_head = new_head

            if snake_head == 0:
                pass
