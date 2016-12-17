#!/usr/bin/python

import curses

import values

class Board:
    grid = []

    def __init__(self, length, height, screen, corners):
        self.length = length
        self.height = height
        self.screen = screen
        self.corners = corners

        for i in range(self.height):
            row = []
            for j in range(self.length):
                row.append(None)
            self.grid.append(row)

    
    def at(self, coords):
        return board[coords[0]][coords[1]]

    
    def draw(self):
        def row_to_string(row):
            item_map = {values.ITEM_FOOD: '*',
                        values.ITEM_SNAKE: 'O'}
            string = ""
            for i in row:
                string += item_map[i]
            return string

        for index, row in enumerate(self.grid):
            self.screen.addstr(self.corners['TOP_LEFT'][0]+index, self.corners['TOP_LEFT'][1],
                               row_to_string(row))
