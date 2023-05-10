from src.game import Game
from src.agents.user_agent import UserAgent
from src.agents.naive_agent import NaiveAgent

window_size = 900, 900
speed = 2
size = 5, 5

agent = NaiveAgent()
game_inst = Game(size, window_size, agent, speed)
print(game_inst.play())