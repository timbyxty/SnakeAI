import torch 
import random 
import snake_gym
import gymnasium as gym
import numpy as np
from collections import deque
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os
import shutil
from snake_gym.envs.snake_env import Tile

class DQNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.BatchNorm2d(1),
            nn.Conv2d(1, 16, 3, 1, 1),
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.Conv2d(16, 32, 3, 1, 1),
            nn.ReLU(),
            nn.BatchNorm2d(32),
            nn.Conv2d(32, 32, 3, 1, 1),
            nn.ReLU(),
            nn.Flatten()
        )
        self.linear = nn.Linear(32*20*20 + 2, 4)
        
    
    def forward(self, x):
        dist = (torch.stack(torch.where(x==Tile.FOOD.value), 1) - torch.stack(torch.where(x==Tile.HEAD.value), 1))[:, 1:]
        x = self.layers(x.unsqueeze(1))
        x = torch.cat([x, dist], 1)
        return self.linear(x)

class QTrainer:
    def __init__(self,model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimer = optim.Adam(model.parameters(), lr = self.lr)    
        self.criterion = nn.MSELoss()

    
    def train_step(self,state,action,reward,next_state,done):
        state = torch.tensor(state,dtype=torch.float)
        next_state = torch.tensor(next_state,dtype=torch.float)
        action = torch.tensor(action,dtype=torch.long)
        reward = torch.tensor(reward,dtype=torch.float)
        done = torch.tensor(done, dtype=torch.bool)

        if len(state.shape) < 3: 
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = torch.unsqueeze(done, 0)
        pred = self.model(state)
        target = pred.clone()
        Q_new = reward.clone()
        not_done = ~done
        Q_new[not_done] = reward[not_done] + self.gamma * pred[not_done].argmax(axis=1)
        target[np.arange(len(target)), action] = Q_new

        self.optimer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimer.step()
         
MAX_MEMORY = 10_000
BATCH_SIZE = 1000


class NeuroAgent:
    _name = "NeuroAgent"
    def __init__(self, name="", LR=0.1):
        self.name = name
        self.inference = False
        self.n_game = 0
        self.epsilon = 1 
        self.gamma = 0.9 
        self.memory = deque(maxlen=MAX_MEMORY) 
        self.model = DQNet()
        self.trainer = QTrainer(self.model,lr=LR,gamma=self.gamma)


    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done)) 

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    def __call__(self, state):
        if(random.random() < self.epsilon) and not self.inference:
            move = random.randint(0, 3)
        else:
            state0 = torch.tensor(state,dtype=torch.float).unsqueeze(0)
            prediction = self.model(state0).flatten()
            move = np.random.choice(np.arange(4), p=torch.softmax(prediction, 0).flatten().detach().numpy())
        return move

    def save(self, info):
        model_folder_path = 'Models'
        file_name = os.path.join(model_folder_path, self.name)
        with open(file_name + "/describtion", "w") as f:
            f.write(info)
        torch.save(self.model.state_dict(), file_name + "/best.pth")
    
    def load(self, path):
        self.inference = True
        self.model.load_state_dict(torch.load(path))
        self.model.eval()

























































































































