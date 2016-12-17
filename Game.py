#!/usr/bin/python

import curses

import values
from Board import Board

class Game:
    current_direction = None


    def __init__(self, config, screen):
        self.config = config
        self.screen = screen


    def start():
        self.board = Board(self.length, self.height, self.screen, self.corners)


    def draw_borders():
        self.screen.addstr(self.corners['TOP_LEFT'][0]-1, self.corners['TOP_LEFT'][1], self.borders['TOP']*x)
        self.screen.addstr(self.corners['BOTTOM_LEFT'][0], self.corners['BOTTOM_LEFT'][1], self.borders['BOTTOM']*x)
        for i in range(self.corners['TOP_LEFT'][0], self.corners['BOTTOM_LEFT'][0]):
            self.screen.addstr(i, self.corners['TOP_LEFT'][1]-1, self.borders['LEFT']) 
            self.screen.addstr(i, self.corners['TOP_RIGHT'][1]+1, self.borders['RIGHT'])


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
