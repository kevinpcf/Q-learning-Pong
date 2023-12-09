import numpy as np
from abc import ABC, abstractmethod

class Agent(ABC):

    def __init__(self, width, height, gamma, alpha):
        self.alpha = alpha
        self.gamma = gamma
        self.height = height
        self.width = width
        self.score = 0

    def normalize_x(self, val):
        ret = 0
        value = int(val)
        if(value < 41):
            ret = -10
        elif(value > self.width - 41):
            ret = -15
        elif(value <= self.width - 41):
            ret = value - 41
        return ret
            
    def normalize_y(self, val):
        value = int(val) 
        if(value > self.height - 6):
            return -5
        elif(value < 65):
            return -5
        else: 
            return value - 65
    
    def normalize_opponent(self, val):
        value = int(val / 5)
        return value - 13
            
class AgentQ(Agent):    
    def __init__(self, width, height, gamma, alpha, epsilon):
        super().__init__(width=width, height=height, gamma=gamma, alpha=alpha)
        self.epsilon = epsilon

        #Posizione y della racchetta, x della palla, y della palla, 3 sono le azioni (movimento sopra, sotto e colpo della palla)
        dimension_opponent = int((height - (height/6) - 65) / 5)
        self.Q = np.zeros((dimension_opponent, width - 80, height - 70, 3))

    def getQ(self):
        return self.Q

class AgentSarsa(Agent):
    def __init__(self, width, height, gamma, alpha):
        super().__init__(width=width, height=height, gamma=gamma, alpha=alpha)

        #Posizione y della racchetta, x della palla, y della palla, 3 sono le azioni (movimento sopra, sotto e colpo della palla)
        dimension_opponent = int((height - (height/6) - 65) / 5)
        self.sarsa = np.zeros((dimension_opponent, width - 80, height - 70, 3))

    def getSarsa(self):
        return self.sarsa
