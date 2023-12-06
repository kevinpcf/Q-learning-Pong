import math
import random

import numpy as np
import pygame

class pongGame:

    def __init__(self):
        """ Inizializzazione dei parametri di gioco"""
        self.width = 720
        self.height = 576
        self.game_speed = 3

        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ping Pong")

        # posizione x e y della palla
        self.xball = self.width/2
        self.yball = self.height/2

        # velocità della palla e angolazione
        self.angle = random.random()*0.5*math.pi+0.75*math.pi
        self.totalSpeed = self.game_speed
        self.ballHDirection = self.totalSpeed*math.cos(self.angle)
        self.ballVDirection = self.totalSpeed*math.sin(self.angle)

        # pozione delle racchette
        self.player_position = self.height/2.4
        self.opponent_position = self.height/2.4

        # paddle length
        self.paddle_length = self.height/6

        self.player_score, self.opponent_score = 0, 0

    def getWidth(self): 
        return self.width

    def getHeight(self): 
        return self.height

    def getState(self):
        """Ritorna i valori degli stati (posizione della racchetta player,
        posizione della racchetta opponent, coordinata x della palla e coordinata y della palla)"""

        return np.array([self.player_position, self.opponent_position, self.xball, self.yball])
    
    def takeAction(self, action):
        # inizializzo la ricompensa a -1
        reward = -1

        # Movimento della racchetta dell'oppenent
        if (action == 0 and self.opponent_position > 5) :
            self.opponent_position = max(5, self.opponent_position - 5)
        elif (action == 1 and self.opponent_position < self.height - 5 - self.paddle_length) :
            self.opponent_position = min(self.height - 5 - self.paddle_length, self.opponent_position + 5)

        # # Movimento della racchetta del giocatore
        if random.random() < 0.3:
            # Simula un errore nel movimento della racchetta
            self.player_position = max(0, min(self.height - self.paddle_length, self.player_position - 5))
        else:
            # Movimento corretto della racchetta
            if self.yball > self.player_position + self.paddle_length / 2:
                self.player_position = min(self.height - self.paddle_length, self.player_position + 5)
            elif self.yball < self.player_position + self.paddle_length / 2:
                self.player_position = max(0, self.player_position - 5)

        # Colpo della palla del player
        if (
            self.yball > self.player_position \
            and self.yball < self.player_position + self.paddle_length \
            and self.xball > 31 \
            and self.xball <= 41
        ):
            self.totalSpeed += 0.2
            self.angle = (
                (math.pi / 4)
                * (self.yball - (self.player_position + self.paddle_length / 2))
                / (self.paddle_length / 2)
            )
            self.xball = 41

        # Colpo della palla dell'opponent
        elif (
            self.yball > self.opponent_position \
            and self.yball < self.opponent_position + self.paddle_length \
            and self.xball > self.width - 40 \
            and self.xball < self.width - 31
        ):
            self.totalSpeed += 0.2
            self.angle = (
                math.pi
                - (math.pi / 4)
                * (self.yball - (self.opponent_position + self.paddle_length / 2))
                / (self.paddle_length / 2)
            )
            self.xball = self.width - 41
            reward = 10

        # se la palla è troppo a sinistra la racchetta ha perso 
        if(self.xball < 41):
            reward = 100
        # se la palla è troppo a destra la racchetta ha vinto
        elif(self.xball > self.width - 40):
            reward = -100

        # se la palla colpisce il bordo inferiore o superiore del gioco
        if(self.yball <= 5 or self.yball >= self.height - 5):
            self.angle = -self.angle

        self.ballHDirection = self.totalSpeed*math.cos(self.angle)
        self.ballVDirection = self.totalSpeed*math.sin(self.angle)
        self.xball = self.xball+self.ballHDirection
        self.yball = self.yball+self.ballVDirection
    
        return reward

    # def takeAction(self, action):
    #     reward = -1

    #     # Movimento della racchetta dell'oppenent
    #     if (action == 0 and self.opponent_position > 5) :
    #         self.opponent_position = max(5, self.opponent_position - 5)

    #         if (self.yball > self.opponent_position \
    #         and self.yball < self.opponent_position + self.paddle_length \
    #         and self.xball > self.width - 40 \
    #         and self.xball < self.width - 31):
    #             self.totalSpeed += 0.2
    #             self.angle = (
    #                 math.pi
    #                 - (math.pi / 4)
    #                 * (self.yball - (self.opponent_position + self.paddle_length / 2))
    #                 / (self.paddle_length / 2)
    #             )
    #             self.xball = self.width - 41
    #             print("colpito")
    #             reward = 10
    #     elif (action == 1 and self.opponent_position < self.height - 5 - self.paddle_length) :
    #         self.opponent_position = min(self.height - 5 - self.paddle_length, self.opponent_position + 5)
    #         if (self.yball > self.opponent_position \
    #         and self.yball < self.opponent_position + self.paddle_length \
    #         and self.xball > self.width - 40 \
    #         and self.xball < self.width - 31):
    #             self.totalSpeed += 0.2
    #             self.angle = (
    #                 math.pi
    #                 - (math.pi / 4)
    #                 * (self.yball - (self.opponent_position + self.paddle_length / 2))
    #                 / (self.paddle_length / 2)
    #             )
    #             self.xball = self.width - 41
    #             reward = 10
    #     elif(action == 2 and self.yball > self.opponent_position \
    #         and self.yball < self.opponent_position + self.paddle_length \
    #         and self.xball > self.width - 40 \
    #         and self.xball < self.width - 31):
    #         self.totalSpeed += 0.2
    #         self.angle = (
    #             math.pi
    #             - (math.pi / 4)
    #             * (self.yball - (self.opponent_position + self.paddle_length / 2))
    #             / (self.paddle_length / 2)
    #         )
    #         self.xball = self.width - 41
    #         reward = 10

    #     if random.random() < 0.3:
    #         self.player_position = max(0, min(self.height - self.paddle_length, self.player_position - 5))
    #     else:
    #         if self.yball > self.player_position + self.paddle_length / 2:
    #             self.player_position = min(self.height - self.paddle_length, self.player_position + 5)
    #         elif self.yball < self.player_position + self.paddle_length / 2:
    #             self.player_position = max(0, self.player_position - 5)

    #     # Colpo della palla del player
    #     if (
    #         self.yball > self.player_position \
    #         and self.yball < self.player_position + self.paddle_length \
    #         and self.xball > 31 \
    #         and self.xball <= 41
    #     ):
    #         self.totalSpeed += 0.2
    #         self.angle = (
    #             (math.pi / 4)
    #             * (self.yball - (self.player_position + self.paddle_length / 2))
    #             / (self.paddle_length / 2)
    #         )
    #         self.xball = 41

    #     # se la palla è troppo a sinistra la racchetta ha perso 
    #     if(self.xball < 41):
    #         reward = 100
    #     # se la palla è troppo a destra la racchetta ha vinto
    #     elif(self.xball > self.width - 40):
    #         reward = -100

    #     # se la palla colpisce il bordo inferiore o superiore del gioco
    #     if(self.yball <= 5 or self.yball >= self.height - 5):
    #         self.angle = -self.angle

    #     self.ballHDirection = self.totalSpeed*math.cos(self.angle)
    #     self.ballVDirection = self.totalSpeed*math.sin(self.angle)
    #     self.xball = self.xball+self.ballHDirection
    #     self.yball = self.yball+self.ballVDirection
        
    #     return reward
        
        
    def draw(self):
        """Disegno delle racchette e della pallina"""
        self.window.fill(0)
        # disegno la palla
        pygame.draw.circle(self.window, (255, 255, 255),
                            (self.xball, self.yball), 5)
        # disegno opponent
        pygame.draw.rect(self.window, (255, 255, 255),
                            (self.width-41, self.opponent_position, 10, self.paddle_length))
        # disegno player
        pygame.draw.rect(self.window, (255, 255, 255),
                            (31, self.player_position, 10, self.paddle_length))
        # aggiorna il display
        pygame.display.flip()
