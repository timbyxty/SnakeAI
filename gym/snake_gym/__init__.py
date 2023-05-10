from gymnasium.envs.registration import register
from snake_gym.envs.snake_env import Tile, Move


register(
    id="snake_gym/Snake-v1.0",
    entry_point="snake_gym.envs:SnakeEnv"
)