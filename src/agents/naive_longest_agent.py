import pygame.event
from snake_gym import Tile
import random
import time

class NaiveLongestPathAgent:
    queue = []
    _name = "NaiveLongestPath"

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
                return p
            if len(p) > len(longest):
                longest = p
            visited.add((x, y))
            s.append(((x - 1, y), p + [0]))
            s.append(((x, y - 1), p + [1]))
            s.append(((x, y + 1), p + [3]))
            s.append(((x + 1, y), p + [2]))
        if value == Tile.TAIL.value:
            if longest:
                return longest
        
    
    def longer_path(self, head, map, path):
        fix_map = map.copy()
        h, w = len(map), len(map[0])
        for _ in range(5):
            x, y = head
            i = 0
            while i < len(path)-1:
                if path[i] == 0:
                    if i and fix_map[x][(y-1)%w] == Tile.EMPTY.value and fix_map[(x-1)%h][(y-1)%w] == Tile.EMPTY.value and path[i+1] != 1 and path[i-1] != 3:
                        fix_map[x][(y-1)%w] = Tile.BODY.value
                        fix_map[(x-1)%h][(y-1)%w] = Tile.BODY.value
                        path.insert(i+1, 3)
                        path.insert(i, 1)
                        i += 2
                    elif i and fix_map[x][(y+1)%w] == Tile.EMPTY.value and fix_map[(x-1)%h][(y+1)%w] == Tile.EMPTY.value and path[i+1] != 3 and path[i-1] != 1:
                        fix_map[x][(y+1)%w] = Tile.BODY.value
                        fix_map[(x-1)%h][(y+1)%w] = Tile.BODY.value
                        path.insert(i+1, 1)
                        path.insert(i, 3)
                        i += 2
                    x = (x - 1)%h
                elif path[i] ==  1: # (0, -1)
                    if i and fix_map[(x+1)%h][y] == Tile.EMPTY.value and fix_map[(x+1)%h][(y-1)%w] == Tile.EMPTY.value and path[i+1] != 2 and path[i-1] != 0:
                        fix_map[(x+1)%h][y] = Tile.BODY.value
                        fix_map[(x+1)%h][(y-1)%w] = Tile.BODY.value
                        path.insert(i+1, 0)
                        path.insert(i, 2)
                        i += 2
                    elif i and fix_map[(x-1)%h][y] == Tile.EMPTY.value and fix_map[(x-1)%h][(y-1)%w] == Tile.EMPTY.value and path[i+1] != 0 and path[i-1] != 2:
                        fix_map[(x-1)%h][y] = Tile.BODY.value
                        fix_map[(x-1)%h][(y-1)%w] = Tile.BODY.value
                        path.insert(i+1, 2)
                        path.insert(i, 0)
                        i += 2
                    y = (y - 1)%w
                elif path[i] ==  3: # (0, 1)
                    if i and fix_map[(x+1)%h][y] == Tile.EMPTY.value and fix_map[(x+1)%h][(y+1)%w] == Tile.EMPTY.value and path[i+1] != 2 and path[i-1] != 0:
                        fix_map[(x+1)%h][y] = Tile.BODY.value
                        fix_map[(x+1)%h][(y+1)%w] = Tile.BODY.value
                        path.insert(i+1, 0)
                        path.insert(i, 2)
                        i += 2
                    elif i and fix_map[(x-1)%h][y] == Tile.EMPTY.value and fix_map[(x-1)%h][(y+1)%w] == Tile.EMPTY.value and path[i+1] != 0 and path[i-1] != 2:
                        fix_map[(x-1)%h][y] = Tile.BODY.value
                        fix_map[(x-1)%h][(y+1)%w] = Tile.BODY.value
                        path.insert(i+1, 2)
                        path.insert(i, 0)
                        i += 2
                    y = (y + 1)%w
                elif path[i] ==  2: # (1, 0)
                    if i and fix_map[x][(y-1)%w] == Tile.EMPTY.value and fix_map[(x+1)%h][(y-1)%w] == Tile.EMPTY.value and path[i+1] != 1 and path[i-1] != 3:
                        fix_map[x][(y-1)%w] = Tile.BODY.value
                        fix_map[(x+1)%h][(y-1)%w] = Tile.BODY.value
                        path.insert(i+1, 3)
                        path.insert(i, 1)
                        i += 2
                    elif i and fix_map[x][(y+1)%w] == Tile.EMPTY.value and fix_map[(x+1)%h][(y+1)%w] == Tile.EMPTY.value and path[i+1] != 3 and path[i-1] != 1:
                        fix_map[x][(y+1)%w] = Tile.BODY.value
                        fix_map[(x+1)%h][(y+1)%w] = Tile.BODY.value
                        path.insert(i+1, 1)
                        path.insert(i, 3)
                        i += 2
                    x = (x + 1)%h
                i += 1
                fix_map[x][y] = Tile.BODY.value

        return path

    def __call__(self, observation):
        if not self.queue:
            map = observation
            head = self.get_pos(map, Tile.HEAD.value)
            move = self.find_move(map, head, Tile.FOOD.value)
            if move is None:
                move = self.find_move(map, head, Tile.TAIL.value)
            if move is None:
                move = [random.choice(range(4))]
            long = self.longer_path(head, map, move)
            self.queue = long
        move =  self.queue.pop(0)
        return move
