from game import Game
from agents.user_agent import User
from agents.naive_agent import Naive

window_size = 900, 900
speed = 50
size = 20, 20

agent = Naive()
game_inst = Game(size, window_size, agent, speed, obstacles=True)
game_inst.play()