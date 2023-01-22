from enum import Enum, auto
from collections import deque
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


TILE_COUNT = 5


class Move(Enum):
    LEFT = auto()
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    NOOP = None


class Rewards(Enum):
    ALIVE = 1
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

        self.observation_space = gym.spaces.Dict({
            "map": gym.spaces.Box(0, TILE_COUNT, shape=self._size, dtype=np.int8)
        })
        self.action_space = gym.spaces.Discrete(4)
        self._action_to_move = {
            Move.LEFT: np.array([-1, 0]),
            Move.UP: np.array([0, -1]),
            Move.DOWN: np.array([0, 1]),
            Move.RIGHT: np.array([1, 0]),
            Move.NOOP: None
        }
        self._empty_poses:int = 0

    def _get_obs(self):
        return {"map": self._map}

    def _get_info(self):
        return {"empty_cells_left": ...}

    def _get_random_empty_pos(self):
        empty = np.vstack(np.where(self._map == Tile.EMPTY.value)).T
        return tuple(empty[np.random.choice(len(empty))])

    def _set_food(self):
        self._map[self._get_random_empty_pos()] = Tile.FOOD.value

    def _set_snake_head(self):
        self._snake = deque()
        head_pos = self._get_random_empty_pos()
        self._map[head_pos] = Tile.HEAD.value
        self._snake.appendleft(head_pos)
        self._empty_poses -= 1

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
        self._set_snake_head()
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

        reward = Rewards.ALIVE
        truncated = False

        self._snake.appendleft(next_head)
        self._map[head] = Tile.BODY.value
        if self._map[next_head] == Tile.FOOD.value:
            reward = Rewards.FED
            self._empty_poses -= 1
            if self._empty_poses != 0:
                self._set_food()
            else:
                truncated = True
        else:
            self._map[self._snake.pop()] = Tile.EMPTY.value
        self._map[next_head] = Tile.HEAD.value

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward.value, False, truncated, info

    def render(self) -> Union[RenderFrame, list[RenderFrame], None]:
        return self._map
