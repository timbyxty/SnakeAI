import pygame
import snake_gym
import gymnasium

pygame.init()
window_size = 900, 900
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
speed = 10

size = 20, 20
cell_size = window_size[0]/size[0], window_size[1]/size[1]

env = gymnasium.make('snake_gym/Snake-v1.0', size=size, obstacles=True)
env.reset()

move = snake_gym.Move.NOOP
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and move != snake_gym.Move.UP:
                move = snake_gym.Move.DOWN
                break
            if event.key == pygame.K_UP and move != snake_gym.Move.DOWN:
                move = snake_gym.Move.UP
                break
            if event.key == pygame.K_LEFT and move != snake_gym.Move.RIGHT:
                move = snake_gym.Move.LEFT
                break
            if event.key == pygame.K_RIGHT and move != snake_gym.Move.LEFT:
                move = snake_gym.Move.RIGHT
                break

    observation, reward, done, _, info = env.step(move)
    if done:
        break
    for x, row in enumerate(observation['map']):
        for y, value in enumerate(row):
            color = pygame.Color(52, 183, 98)
            if value == snake_gym.Tile.FOOD.value:
                color = pygame.Color(255, 0, 0)
            elif value == snake_gym.Tile.HEAD.value:
                color = pygame.Color(158, 130, 17)
            elif value == snake_gym.Tile.BODY.value:
                color = pygame.Color(229, 198, 72)
            elif value == snake_gym.Tile.OBSTACLE.value:
                color = pygame.Color(0, 0, 0)
            position = x*cell_size[0], y*cell_size[1]
            pygame.draw.rect(screen, rect=pygame.rect.Rect(*position, *cell_size), color=color)
    clock.tick(speed)
    pygame.display.flip()
pygame.quit()
