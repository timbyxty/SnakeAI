from game import Game
from agents.user_agent import User

window_size = 900, 900
speed = 20
size = 20, 20

agent = User()
game_inst = Game(size, window_size, agent, speed)
game_inst.play()