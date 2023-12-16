import numpy as np
from abc import ABC

class Agent(ABC):
    """Classe astratta per gli agenti"""
    def __init__(self, width, height, gamma, alpha):
        self.alpha = alpha
        self.gamma = gamma
        self.height = height
        self.width = width
        self.score = 0
    
    def normalize_x(self, val):
        """Funzione che mappa la coordinata x della palla nel corrispettivo stato"""
        # 1 stato corrisponde a 8 pixel dello schermo
        v = int(np.floor((val/self.width) * 50)) - 4
        if(v < 0):
            v = 0
        if (v >= 42):
            v = 42 - 1
        return v
            
    def normalize_y(self, val):
        """Funzione che mappa la coordinata y della palla o della racchetta nel corrispettivo stato"""
        # 1 stato corrisponde a 8 pixel dello schermo
        v = int(np.floor(((val + 4) / self.height) * 50)) - 8
        if(v < 0):
            v = 0
        if v >= 40:
            v = 40 - 1
        return v
                
class AgentQ(Agent):
    """Classe per agente di tipo Q-learning""" 
    def __init__(self, width, height, gamma, alpha, epsilon):
        super().__init__(width=width, height=height, gamma=gamma, alpha=alpha)
        self.epsilon = epsilon

        #Posizione y della racchetta, x della palla, y della palla, 3 azioni (movimento sopra, sotto e colpo della palla)
        self.Q = np.zeros((40, 42, 40, 3))


class AgentSarsa(Agent):
    """Classe per agente di tipo SARSA""" 
    def __init__(self, width, height, gamma, alpha):
        super().__init__(width=width, height=height, gamma=gamma, alpha=alpha)

        #Posizione y della racchetta, x della palla, y della palla, 3 azioni (movimento sopra, sotto e colpo della palla)
        self.sarsa = np.zeros((40, 42, 40, 3))
