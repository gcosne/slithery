#!/usr/bin/python

import random

from Board import Board

class BaseItem:
    def __init__(self):
        pass

    
    def get_spawn(self, board):
        while True:
            # Spawn at least a quarter into the board
            spawn_coords = (random.randint((1/4)*board.height, (3/4)*board.height), 
                            random.randint((1/4)*board.length, (3/4)*board.length))

            # Ensure there are no other powerups occupying the same spot
            if board.at(spawn_coords) is None:
                return spawn_coords
