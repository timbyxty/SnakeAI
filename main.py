from src.game import Game
from src.agents.user_agent import UserAgent
from src.agents.naive_agent import NaiveAgent
from src.agents.naive_longest_agent import NaiveLongestPathAgent
from src.agents.neuro_agent import NeuroAgent

window_size = 900, 900
speed = 10
size = 20, 20

agent = NaiveLongestPathAgent()
# agent = NeuroAgent()
# agent.load("/Users/timbyxty/SnakeAI-1/Models/20x20_LR=0.001/best.pth")
# results = []
# for i in range(100):
game_inst = Game(size, window_size, agent, speed, obstacles=True, draw=False)
game_inst.play()
# print(results)