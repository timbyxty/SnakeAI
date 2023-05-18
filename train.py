from src.agents.neuro_agent import NeuroAgent
import gymnasium as gym
import os
import shutil
import matplotlib.pyplot as plt 
import numpy as np

plt.ion()

def plot(scores, mean_scores, name=False):
    plt.clf()
    plt.title("Training...")
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores, alpha=0.75)
    plt.plot(mean_scores)
    plt.text(len(scores)-1,scores[-1],str(scores[-1]))
    plt.text(len(mean_scores)-1,mean_scores[-1],str(mean_scores[-1]))
    plt.pause(.05)
    if name:
        plt.savefig(name)
    else:
        plt.show(block=False)
    

LR = 0.01
exp_name = f"5x5_{LR=}"
if os.path.isdir(f"Models/{exp_name}"):
    shutil.rmtree(f"Models/{exp_name}")
os.mkdir(f"Models/{exp_name}")

plot_scores = []
plot_mean_scores = []
record = float("-inf")
agent = NeuroAgent(exp_name, LR)
env = gym.make('snake_gym/Snake-v1.0', size=(5, 5), obstacles=False)
state, _  = env.reset()
score = 0
step = 0
while True:
    if agent.n_game == 2000:
        break
    state_old = state.copy()
    action = agent(state_old)
    state, reward, done, _, _ = env.step(action)
    score += reward
    # train short memory
    agent.train_short_memory(state_old, action,reward, state,done)

    #remember
    agent.remember(state_old, action,reward, state,done)
    if step == 1000:
        done = True
        step = 0
    if done :
        # Train long memory,plot result
        state, _ = env.reset()
        agent.n_game += 1
        agent.epsilon *= 0.97
        agent.train_long_memory()
        plot_scores.append(score)
        score = 0
        mean_score = np.mean(plot_scores[-50:])
        plot_mean_scores.append(mean_score)
        if mean_score > record:
            print(agent.epsilon)
            # plot(plot_scores, plot_mean_scores)

            record = mean_score
            agent.save(f"{mean_score=}_{agent.n_game}")
            print("saved")
    step += 1

plot(plot_scores, plot_mean_scores, f"Models/{exp_name}.png")
