import gymnasium
import pygame.event
from snake_gym import Tile


class Game:
    _tile_to_color = {
        Tile.OBSTACLE.value: pygame.Color(0, 0, 0),
        Tile.EMPTY.value: pygame.Color(52, 183, 98),
        Tile.FOOD.value: pygame.Color(255, 0, 0),
        Tile.BODY.value: pygame.Color(229, 198, 72),
        Tile.HEAD.value: pygame.Color(158, 130, 17)
    }
    def __init__(self, size, window_size, agent, speed=10, obstacles=False):
        self.size = size
        self.speed = speed
        self.agent = agent
        self.cell_size = window_size[0]/size[0], window_size[1]/size[1]
        self.obstacles = obstacles
        self.env = gymnasium.make('snake_gym/Snake-v1.0', size=size, obstacles=obstacles)

        pygame.init()

        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()

    def play(self):
        observation, info = self.env.reset()
        self._draw(observation['map'])
        self.clock.tick(self.speed)
        pygame.display.flip()
        truncated = False
        while True:
            if not truncated:
                action = self.agent(observation)

                observation, reward, done, truncated, info = self.env.step(action)

                if done:
                    break
            self._draw(observation['map'])
            self.clock.tick(self.speed)
            pygame.display.flip()

    def _draw(self, state):
        for x, row in enumerate(state):
            for y, value in enumerate(row):
                color = self._tile_to_color[value]
                position = x * self.cell_size[0], y * self.cell_size[1]
                pygame.draw.rect(self.screen, rect=pygame.rect.Rect(*position, *self.cell_size), color=color)
