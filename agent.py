import numpy as np
from abc import ABC

class Agent(ABC):

    def __init__(self, width, height, gamma, alpha):
        self.alpha = alpha
        self.gamma = gamma
        self.height = height
        self.width = width
        self.score = 0
    
    def normalize_x(self, val):
        """Funzione che mappa la coordinata x della palla nel corrispettivo stato"""
        v = int(np.floor((val/400)*20)) - 1
        if(v < 0):
            v = 0
        if v >= 18:
            v = 18-1
        return v
            
    def normalize_y(self, val):
        """Funzione che mappa la coordinata y della palla o della racchetta nel corrispettivo stato"""
        v = int(np.floor((val/400)*20)) - 3
        if(v < 0):
            v = 0
        if v >= 16:
            v = 16-1
        return v
                
class AgentQ(Agent):
    """Classe per agente di tipo Q-learning""" 
    def __init__(self, width, height, gamma, alpha, epsilon):
        super().__init__(width=width, height=height, gamma=gamma, alpha=alpha)
        self.epsilon = epsilon

        #Posizione y della racchetta, x della palla, y della palla, 3 sono le azioni (movimento sopra, sotto e colpo della palla)
        self.Q = np.zeros((16, 18, 16, 3))
    
    def set_terminal_state_Q(self, terminal_left, terminal_right):
        self.Q[:, 0, :, :] = terminal_left
        self.Q[:, self.width -81, :, :] = terminal_right


class AgentSarsa(Agent):
    """Classe per agente di tipo SARSA""" 
    def __init__(self, width, height, gamma, alpha):
        super().__init__(width=width, height=height, gamma=gamma, alpha=alpha)

        #Posizione y della racchetta, x della palla, y della palla, 3 sono le azioni (movimento sopra, sotto e colpo della palla)
        self.sarsa = np.zeros((16, 18, 16, 3))
