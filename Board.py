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
                row.append(None)
            self.grid.append(row)

    
    def at(self, coords):
        return grid[coords[0]][coords[1]]

    
    def draw(self):
        def row_to_string(row):
            item_map = {values.ITEM_FOOD: config['snake'],
                        values.ITEM_SNAKE: config['food']}
            string = ""
            for i in row:
                string += item_map[i]
            return string

        for index, row in enumerate(self.grid):
            self.screen.addstr(values.CORNERS['top_left'][0]+index, values.CORNERS['top_left'][1],
                               row_to_string(row))
