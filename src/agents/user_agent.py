import pygame.event
from snake_gym import Move

class UserAgent:
    last_move = None

    def __call__(self, *args, **kwargs):
        value = self.last_move
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_LEFT:
                value = 0
            if event.key == pygame.K_UP:
                value = 1
            if event.key == pygame.K_RIGHT:
                value = 2
            if event.key == pygame.K_DOWN:
                value = 3
        if value is not None and (value + 2) % 4 != self.last_move:
            self.last_move = value
        else:
            value = self.last_move
        return Move(value)