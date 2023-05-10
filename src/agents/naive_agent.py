import pygame.event
from snake_gym import Tile, Move
import random
import time

class NaiveAgent:
    queue = []
    _name = "Naive"
    @staticmethod
    def get_pos(map, value):
        for x, row in enumerate(map):
            for y, v in enumerate(row):
                if v == value:
                    return x, y

    @staticmethod
    def find_move(map, start, value):
        s = [(start, [])]
        visited = set()
        longest = []
        while s:
            (x, y), p = s.pop(0)
            x = x % len(map)
            y = y % len(map[x])
            if (x, y) != start:
                if map[x][y] != value and map[x][y] != Tile.EMPTY.value:
                    continue
            if (x, y) in visited:
                continue
            if map[x][y] == value:
                return p[0]
            if len(p) > len(longest):
                longest = p
            visited.add((x, y))
            s.append(((x - 1, y), p + [0]))
            s.append(((x, y - 1), p + [1]))
            s.append(((x, y + 1), p + [3]))
            s.append(((x + 1, y), p + [2]))
        if value == Tile.TAIL.value:
            if longest:
                return longest[0]

    def __call__(self, observation):
        map = observation
        head = self.get_pos(map, Tile.HEAD.value)
        move = self.find_move(map, head, Tile.FOOD.value)
        if move is None:
            move = NaiveAgent.find_move(map, head, Tile.TAIL.value)
        if move is None:
            move = random.choice(range(4))
        return Move(move)
