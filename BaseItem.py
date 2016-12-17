#!/usr/bin/python

import random

from Board import Board

class BaseItem:
    def __init__(self):
        pass

    
    def get_spawn(self, board):
        while True:
            spawn_coords = (random.randint((1/4)*board.height, (3/4)*board.height), 
                            random.randint((1/4)*board.length, (3/4)*board.length))

            if board.at(spawn_coords) is None:
                return spawn_coords
