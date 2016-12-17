#!/usr/bin/python

import curses

import values


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

        for key, value in items.iteritems():
            item_map = {values.ITEM_FOOD: config['snake'],
                        values.ITEM_SNAKE: config['food']}

            for i in value:
                replace(item_map[key], i)
