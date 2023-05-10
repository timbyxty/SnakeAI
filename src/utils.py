import random
import numpy as np
from datetime import datetime
import pickle


class ReplayBuffer(object):

    @staticmethod
    def from_pickle(filepath):
        with open(filepath, "rb") as f:
            return pickle.load(f)

    def __init__(self, size):
        self._storage = []
        self._maxsize = size

    def __len__(self):
        return len(self._storage)

    def add(self, obs_t, action, reward, obs_tp1, done):
        data = (obs_t, action, reward, obs_tp1, done)

        if len(self._storage) == self._maxsize: 
            self._storage.remove(self._storage[0])
        self._storage.append(data) 

    def sample(self, batch_size):
        idxes = np.random.choice(len(self._storage), batch_size) # 
        full_batch = [self._storage[idxes[i]] for i in range(batch_size)]
        states,actions,rewards,next_states,is_done = [],[],[],[],[]
        
        for state, action, reward, next_state, done in full_batch:
            states.append(state)
            actions.append(action)
            rewards.append(reward)
            next_states.append(next_state)
            is_done.append(done)
        
        return np.array(states), np.array(actions), np.array(rewards), np.array(next_states), np.array(is_done)
    
    def save(self, name):
        with open(f"{name}-{datetime.now()}.pkl", "wb") as f:
            pickle.dump(self, f)
