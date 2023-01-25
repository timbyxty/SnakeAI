import pygame.event

from snake_gym import Move

class User:

    def __call__(self, *args, **kwargs):
        for event in reversed(pygame.event.get(eventtype=pygame.KEYDOWN)):
            if event.key == pygame.K_DOWN:
                return Move.DOWN
            if event.key == pygame.K_UP:
                return Move.UP
            if event.key == pygame.K_LEFT:
                return Move.LEFT
            if event.key == pygame.K_RIGHT:
                return Move.RIGHT

        return Move.NOOP