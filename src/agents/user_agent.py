import pygame.event


class User:

    def __call__(self, *args, **kwargs):
        for event in pygame.event.get(eventtype=pygame.KEYDOWN):
            if event.key == pygame.K_LEFT:
                return 0
            if event.key == pygame.K_UP:
                return 1
            if event.key == pygame.K_RIGHT:
                return 2
            if event.key == pygame.K_DOWN:
                return 3

        return None