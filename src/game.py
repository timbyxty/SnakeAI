from enum import Enum, auto
from collections import deque
import random
from copy import deepcopy
from typing import Optional


class Tile(Enum):
    EMPTY = auto()
    FOOD = auto()
    OBSTACLE = auto()
    HEAD = auto()
    BODY = auto()


class Move(Enum):
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    RIGHT = auto()


class Game:
    def __init__(self, size=(20, 20), obstacles=False):
        self.height: int
        self.width: int
        self.snake: deque = deque()
        self.height, self.width = size
        self.obstacles: bool = obstacles
        self.map: list[list[Tile]] = [[Tile.EMPTY for _ in range(self.height)] for _ in range(self.width)]

    def set_food(self) -> None:
        empty_positions = []
        for x in range(self.height):
            for y in range(self.width):
                if self.map[x][y] == Tile.EMPTY and (x, y) not in self.snake:
                    empty_positions.append((x, y))
        food_position = random.choice(empty_positions)
        self.map[food_position[0]][food_position[1]] = Tile.FOOD

    def init_game(self) -> None:
        x, y = random.randint(1, self.height - 1), random.randint(1, self.width - 1)
        self.snake.append((x, y))
        self.set_food()

    def move(self, move: Optional[Move]) -> tuple[bool, list[list[Tile]]]:
        if move is None:
            return True, self.get_map
        position = self.snake[-1]
        if move == Move.LEFT:
            next_head = position[0] - 1, position[1]
        elif move == Move.UP:
            next_head = position[0], position[1] - 1
        elif move == Move.RIGHT:
            next_head = position[0] + 1, position[1]
        elif move == Move.DOWN:
            next_head = position[0], position[1] + 1
        else:
            raise ValueError
        next_head = next_head[0] % self.height, next_head[1] % self.width
        if next_head in self.snake or self.map[next_head[0]][next_head[1]] == Tile.OBSTACLE:
            return False, self.get_map

        self.snake.append(next_head)
        if self.map[next_head[0]][next_head[1]] == Tile.FOOD:
            self.map[next_head[0]][next_head[1]] = Tile.EMPTY
            self.set_food()
        else:
            self.snake.popleft()
        return True, self.get_map

    @property
    def get_map(self):
        current_map = deepcopy(self.map)
        for i, (x, y) in enumerate(self.snake):
            if i == len(self.snake) - 1:
                current_map[x][y] = Tile.HEAD
            else:
                current_map[x][y] = Tile.BODY
        return current_map
