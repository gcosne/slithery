#!/usr/bin/python

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
