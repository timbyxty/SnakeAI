# import pygame
# import game
#
# pygame.init()
# window_size = 900, 900
# screen = pygame.display.set_mode(window_size)
# clock = pygame.time.Clock()
# speed = 5
#
# size = 20, 20
# cell_size = window_size[0]/size[0], window_size[1]/size[1]
#
# snake = game.Game(size)
# snake.reset()
#
# move = None
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#             break
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_DOWN and move != game.Move.UP:
#                 move = game.Move.DOWN
#             if event.key == pygame.K_UP and move != game.Move.DOWN:
#                 move = game.Move.UP
#             if event.key == pygame.K_LEFT and move != game.Move.RIGHT:
#                 move = game.Move.LEFT
#             if event.key == pygame.K_RIGHT and move != game.Move.LEFT:
#                 move = game.Move.RIGHT
#
#     status, cur_map = snake.step(move)
#     if not status:
#         break
#     for x, row in enumerate(cur_map):
#         for y, value in enumerate(row):
#             color = pygame.Color(52, 183, 98)
#             if value == game.Tile.FOOD:
#                 color = pygame.Color(255, 0, 0)
#             elif value == game.Tile.HEAD:
#                 color = pygame.Color(158, 130, 17)
#             elif value == game.Tile.BODY:
#                 color = pygame.Color(229, 198, 72)
#             position = x*cell_size[0], y*cell_size[1]
#             pygame.draw.rect(screen, rect=pygame.rect.Rect(*position, *cell_size), color=color)
#     clock.tick(speed)
#     pygame.display.flip()
# pygame.quit()
#

import game

g = game.Game()
obs, info = g.reset()
done = False
truncated = False
print(obs['map'])
while not done and not truncated:
    obs, reward, done, truncated, info = g.step(game.Move(int(input())))
    print(obs['map'], reward)
