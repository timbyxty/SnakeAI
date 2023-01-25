import pygame
from game import Game
from agents.user_agent import User
pygame.init()
window_size = 900, 900
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
speed = 10

size = 20, 20
cell_size = window_size[0]/size[0], window_size[1]/size[1]
agent = User()
game_inst = Game(size, window_size, agent, speed)
game_inst.play()