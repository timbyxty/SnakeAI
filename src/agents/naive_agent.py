import pygame.event
from snake_gym import Tile


class Naive:
    queue = []

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

        while s:
            (x, y), p = s.pop(0)
            x = x % len(map)
            y = y % len(map[x])
            if (x, y) != start:
                if map[x][y] != Tile.FOOD.value and map[x][y] != Tile.EMPTY.value:
                    continue
            if (x, y) in visited:
                continue
            if map[x][y] == value:
                # return p
                return p[0]
            visited.add((x, y))
            s.append(((x - 1, y), p + [0]))
            s.append(((x, y - 1), p + [1]))
            s.append(((x, y + 1), p + [3]))
            s.append(((x + 1, y), p + [2]))

    def __call__(self, observation):
        # if self.queue:
        #     move = self.queue.pop(0)
        #     return move
        # if self.queue is None:
        #     return 0
        map = observation['map']
        head = self.get_pos(map, Tile.HEAD.value)
        # self.queue = self.find_move(map, head, Tile.FOOD.value)
        # return self.__call__(observation)
        move = self.find_move(map, head, Tile.FOOD.value)
        return move
