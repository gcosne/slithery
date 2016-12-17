#!/usr/bin/python

import random

import values
from Board import Board


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
