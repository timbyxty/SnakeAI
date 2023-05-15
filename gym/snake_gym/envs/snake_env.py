from enum import Enum, auto
from collections import deque
import random
from copy import deepcopy
from typing import Optional, Union
import gymnasium as gym
import numpy as np
from gymnasium.core import RenderFrame

class Tile(Enum):
    EMPTY = 0
    FOOD = 1
    OBSTACLE = 2
    HEAD = 3
    BODY = 4
    TAIL = 5


TILE_COUNT = 6


class Move(Enum):
    NOOP = None
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3


class Rewards(Enum):
    ALIVE = -1
    FED = 10
    DIED = -100
    IDLE = 0


class SnakeEnv(gym.Env):

    def __init__(self, size=(5, 5), obstacles=False):
        self._size = np.array(size)
        self._snake: deque = deque()
        self._obstacles: bool = obstacles
        self._obstacles_limit = np.prod(self._size) // 25
        self._map = np.zeros(self._size, dtype=np.int8)
        self.observation_space = gym.spaces.Box(0, TILE_COUNT, shape=self._size, dtype=np.int8)
        self.action_space = gym.spaces.Discrete(4)
        self._action_to_move = {
            0: np.array([-1, 0]),
            1: np.array([0, -1]),
            3: np.array([0, 1]),
            2: np.array([1, 0]),
            None: None
        }
        self._empty_poses:int = 0

    def _get_obs(self):
        return self._map

    def _get_info(self):
        return {"empty_cells_left": ...}

    def _get_random_empty_pos(self):
        empty = np.vstack(np.where(self._map == Tile.EMPTY.value)).T
        return tuple(empty[np.random.choice(len(empty))])

    def _set_food(self):
        self._map[self._get_random_empty_pos()] = Tile.FOOD.value

    def _set_snake(self):
        self._snake = deque()
        head_pos = self._get_random_empty_pos()
        body_pos = ((head_pos[0] + 1)%self._size[0] , head_pos[1])
        tail_pos = ((head_pos[0] + 2)%self._size[0] , head_pos[1])
        self._map[head_pos] = Tile.HEAD.value
        self._map[body_pos] = Tile.BODY.value
        self._map[tail_pos] = Tile.TAIL.value
        self._snake.extendleft([tail_pos, body_pos, head_pos])
        self._empty_poses -= 3

    def _set_obstacle(self):
        if self._obstacles:
            for _ in range(self._obstacles_limit):
                obstacle_pos = self._get_random_empty_pos()
                self._map[obstacle_pos] = Tile.OBSTACLE.value
                self._empty_poses -= 1


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._empty_poses = np.prod(self._size)
        self._map.fill(Tile.EMPTY.value)
        self._set_snake()
        self._set_food()
        self._set_obstacle()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def step(self, action):
        head = self._snake[0]
        action = self._action_to_move[action]
        if action is None:
            return self._get_obs(), Rewards.IDLE.value, False, False, self._get_info()
        next_head = tuple((head + action) % self._size)
        if (next_head in self._snake and next_head != self._snake[-1]) or self._map[next_head] == Tile.OBSTACLE.value:
            observation = self._get_obs()
            info = self._get_info()
            return observation, Rewards.DIED.value, True, False, info

        reward = Rewards.ALIVE.value
        truncated = False


        self._snake.appendleft(next_head)
        self._map[head] = Tile.BODY.value

        if self._map[next_head] == Tile.FOOD.value:
            reward = Rewards.FED.value
            self._empty_poses -= 1
            if self._empty_poses != 0:
                self._set_food()
            else:
                observation = self._get_obs()
                info = self._get_info()
                return observation, reward, True, True, info
        else:
            self._map[self._snake.pop()] = Tile.EMPTY.value
        self._map[next_head] = Tile.HEAD.value
        self._map[self._snake[-1]] = Tile.TAIL.value

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, False, truncated, info

    def render(self) -> Union[RenderFrame, list[RenderFrame], None]:
        return self._map
