import numpy as np
import random
from pongGame import pongGame

class Agent:

    def __init__(self, height, width, alpha=0.5, epsilon=0.6):
        self.alpha = alpha
        self.epsilon = epsilon

        #Posizione y della racchetta, x della palla, y della palla, 3 sono le azioni (movimento sopra, sotto e colpo della palla)
        self.Q = np.zeros((height - 10, width - 80, height - 10, 3))

    def run_learning_episode(self) -> None:
        pong = pongGame()

        finish = False

        while(not finish):
            # prendo gli stati della racchetta giocatore e le coordinate della palla 
            _, opponent_position, xball, yball = pong.getState()

            opponent_position = self.normalize_y(opponent_position)
            xball = self.normalize_x(xball)
            yball = self.normalize_y(yball)

            action_values = self.Q[opponent_position, xball, yball]

            # scelgo un valore randomico
            random_greedy = random.random()
            # se il valore è maggiore di epsilon faccio exploitation
            if(random_greedy > self.epsilon):
                action = np.argmax(action_values)
            # altrimenti faccio exploration
            else:
                action = random.randint(0,2)

            print(action)
            # svolgere le azioni
            reward = pong.takeAction(action)

            # inizializzo i nuovi stati
            _, new_opponent_position, new_xball, new_yball = pong.getState()

            new_opponent_position = self.normalize_y(new_opponent_position)
            new_xball = self.normalize_x(new_xball)
            new_yball = self.normalize_y(new_yball)

            # aggiorno la funzione Q learning
            #capire se mettere il fattore di costo

            self.Q[opponent_position, xball, yball, action] = self.Q[opponent_position, xball, yball, action] + \
                self.alpha * (reward + max(self.Q[new_opponent_position, new_xball, new_yball]) - \
                    self.Q[opponent_position, xball, yball, action])
            
            print(self.Q[opponent_position, xball, yball, action])
            
            # FARE GESTIONE UPDATE STATI


            if(reward == 100 or reward == -100):
                finish = True

            pong.draw()


    def normalize_x(self, val):
        value = int(val)
        if(value > 943):
            return 943
        else: 
            return value
        
    def normalize_y(self, val):
        value = int(val)
        if(value > 757):
            return 757
        else: 
            return value
        