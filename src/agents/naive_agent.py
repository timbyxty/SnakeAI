import pygame.event
from snake_gym import Tile

class Naive:
    @staticmethod
    def get_head_pos(map):
        for x, row in enumerate(map):
            for y, v in enumerate(row):
                if v == Tile.HEAD.value:
                    return x, y

    def __call__(self, observation):
        map = observation['map']
        x, y = self.get_head_pos()
        empty_value = Tile.EMPTY.value
        if map[x][y-1] == empty_value:
            return 0
        elif map[x-1][y] == empty_value:
            return 1
        elif map[x][y+1] == empty_value:
            return 2
        else: 
            return 3
