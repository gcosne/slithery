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
