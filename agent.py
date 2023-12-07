import numpy as np
import random

import pygame
from pongGame import pongGame
import joblib

class Agent:

    def __init__(self, width, height, gamma=0.5, alpha=0.5, epsilon=0.2):
        self.alpha = alpha
        self.epsilon = epsilon
        self.gamma = gamma
        self.height = height
        self.width = width

        self.player_score = 0
        self.opponent_score = 0

        #Posizione y della racchetta, x della palla, y della palla, 3 sono le azioni (movimento sopra, sotto e colpo della palla)
        dimension_opponent = int((height - (height/6) - 65) / 5)
        print("DImension", dimension_opponent)
        self.Q = np.zeros((dimension_opponent, width - 80, height - 70, 3))

    def run_learning_episode(self):
        pong = pongGame()

        finish = False

        while(not finish):
            # prendo gli stati della racchetta giocatore e le coordinate della palla 
            _, opponent_position, xball, yball = pong.getState()
            opponent_position = self.normalize_opponent(opponent_position)
            xball = self.normalize_x(xball)
            yball = self.normalize_y(yball)

            if (xball != -10 and xball != -15):
                action_values = self.Q[opponent_position, xball, yball]

                # scelgo un valore randomico
                random_greedy = random.random()
                # se il valore è maggiore di epsilon faccio exploitation
                if(random_greedy > self.epsilon):
                    action = np.argmax(action_values)
                # altrimenti faccio exploration
                else:
                    action = random.randint(0,2)
            else:
                action = 0
                    
            reward = pong.takeAction(action)

            # inizializzo i nuovi stati
            _, new_opponent_position, new_xball, new_yball = pong.getState()

            new_opponent_position = self.normalize_opponent(new_opponent_position)
            new_xball = self.normalize_x(new_xball)
            new_yball = self.normalize_y(new_yball)

            if new_xball != -10 and new_xball != -15:
                self.Q[opponent_position, xball, yball, action] = self.Q[opponent_position, xball, yball, action] + \
                    self.alpha * (reward + (self.gamma * max(self.Q[new_opponent_position, new_xball, new_yball])) - \
                        self.Q[opponent_position, xball, yball, action])

            if(reward == 100):
                self.opponent_score = self.opponent_score + 1
                finish = True
            elif(reward == -100):
                self.player_score = self.player_score + 1
                finish = True

            pong.draw(self.player_score, self.opponent_score)
    
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

    def save(self):
        """ Funzione per salvare il modello """
        result = {'Q': self.Q, 'player_score': self.player_score, 'opponent_score': self.opponent_score}

        # Salva come file joblib con compressione
        joblib.dump(result, "training.joblib", compress=('zlib', 3))
        print("File salvato correttamente")
            

