import math
import random
import numpy as np
import pygame

class pongGame:

    def __init__(self):
        """ Inizializzazione dei parametri di gioco"""
        self.width = 400
        self.height = 400
        self.game_speed = 0.5

        # Inizializzazione della finestra di gioco
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ping Pong")

        # posizione x e y della palla
        self.xball = self.width/2
        self.yball = self.height/2

        # velocità e angolazione della palla
        direction = random.choice([0, 1])
        self.angle = random.random() * 0.5 * math.pi + 0.75 * math.pi
        if direction == 1:
            self.angle = (0.25 * math.pi) - random.random() * 0.5 * math.pi

        self.totalSpeed = self.game_speed
        self.ballHDirection = self.totalSpeed * math.cos(self.angle)
        self.ballVDirection = self.totalSpeed * math.sin(self.angle)

        # pozione delle racchette
        self.agent_1_position = self.height/2.4
        self.agent_2_position = self.height/2.4

        # lunghezza della racchetta
        self.paddle_length = self.height/6

    def getWidth(self): 
        """Ritorna la lunghezza dello schermo"""
        return self.width

    def getHeight(self): 
        """Ritorna l'altezza dello schermo"""
        return self.height

    def getState(self):
        """Ritorna i valori degli stati (posizione della racchetta sinistra,
        posizione della racchetta destra, posizione x della palla e posizione y della palla)"""

        return np.array([self.agent_1_position, self.agent_2_position, self.xball, self.yball])

    def takeAction(self, action1, action2):
        """Svolge l'azione delle racchette ed ottiene le ricompense"""
        reward1 = 0
        reward2 = 0
        
        # movimento della racchetta sinistra
        # se la racchetta deve salire di 5 punti
        if (action1 == 1 and self.agent_1_position > 65) :
            self.agent_1_position = self.agent_1_position - 5

            if (self.yball > self.agent_1_position \
            and self.yball < self.agent_1_position + self.paddle_length \
            and self.xball > 30 \
            and self.xball < 40):
                self.angle = (
                    (math.pi / 4)
                    * (self.yball - (self.agent_1_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = 40
                reward1 = 5
            elif (self.yball > self.agent_1_position \
                and self.yball < self.agent_1_position + self.paddle_length \
                and self.xball > 40):
                    reward1 = 10
            else:
                reward1 = -1

        # se la racchetta deve scendere di 5 punti
        elif (action1 == 2 and self.agent_1_position < self.height - 25 - self.paddle_length) :
            self.agent_1_position = self.agent_1_position + 5
            if (self.yball > self.agent_1_position \
            and self.yball < self.agent_1_position + self.paddle_length \
            and self.xball > 30 \
            and self.xball < 40):
                self.angle = (
                    (math.pi / 4)
                    * (self.yball - (self.agent_1_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = 40
                reward1 = 5
            elif (self.yball > self.agent_1_position \
                and self.yball < self.agent_1_position + self.paddle_length \
                and self.xball > 40):
                    reward1 = 10
            else:
                reward1 = -1

        # se la racchetta deve restare ferma
        elif(action1 == 0):
            if(self.yball > self.agent_1_position \
            and self.yball < self.agent_1_position + self.paddle_length \
            and self.xball > 30 \
            and self.xball < 40):
                self.angle = (
                    (math.pi / 4)
                    * (self.yball - (self.agent_1_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = 40
                reward1 = 5
            elif (self.yball > self.agent_1_position \
                and self.yball < self.agent_1_position + self.paddle_length \
                and self.xball > 40):
                    reward1 = 10
            else:
                reward1 = -1

        # Movimento della racchetta destra
        # se la racchetta deve scendere di 5 punti
        if (action2 == 1 and self.agent_2_position > 65) :
            self.agent_2_position = self.agent_2_position - 5

            if (self.yball > self.agent_2_position \
            and self.yball < self.agent_2_position + self.paddle_length \
            and self.xball > self.width - 40 \
            and self.xball < self.width - 30):
                self.angle = (
                    math.pi
                    - (math.pi / 4)
                    * (self.yball - (self.agent_2_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = self.width - 40
                reward2 = 5
            elif (self.yball > self.agent_2_position \
                and self.yball < self.agent_2_position + self.paddle_length \
                and self.xball < self.width - 40):
                    reward2 = 10
            else:
                reward2 = -1

        # se la racchetta deve salire di 5 punti
        elif (action2 == 2 and self.agent_2_position < self.height - 25 - self.paddle_length) :
            self.agent_2_position = self.agent_2_position + 5
            if (self.yball > self.agent_2_position \
            and self.yball < self.agent_2_position + self.paddle_length \
            and self.xball > self.width - 40 \
            and self.xball < self.width - 30):
                self.angle = (
                    math.pi
                    - (math.pi / 4)
                    * (self.yball - (self.agent_2_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = self.width - 40
                reward2 = 5
            elif (self.yball > self.agent_2_position \
                and self.yball < self.agent_2_position + self.paddle_length \
                and self.xball < self.width - 40):
                    reward2 = 10
            else:
                reward2 = -1

        # se la racchetta deve restare ferma
        elif(action2 == 0):
            if(self.yball > self.agent_2_position \
            and self.yball < self.agent_2_position + self.paddle_length \
            and self.xball > self.width - 40 \
            and self.xball < self.width - 30):
                self.angle = (
                    math.pi
                    - (math.pi / 4)
                    * (self.yball - (self.agent_2_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = self.width - 40
                reward2 = 5
            elif (self.yball > self.agent_2_position \
                and self.yball < self.agent_2_position + self.paddle_length \
                and self.xball < self.width - 40):
                    reward2 = 10
            else:
                reward2 = -1

        # se la palla è troppo a sinistra la racchetta di destra ha vinto 
        if(self.xball < 36):
            reward1 = -8 
            reward2 = 8
        # se la palla è troppo a destra la racchetta di sinistra ha vinto 
        elif(self.xball > self.width - 36):
            reward1 = 8
            reward2 = -8

        # se la palla colpisce il bordo inferiore o superiore del gioco cambio la sua angolazione
        if(self.yball <= 60 or self.yball >= self.height - 20):
            self.angle = -self.angle

        self.ballHDirection = self.totalSpeed*math.cos(self.angle)
        self.ballVDirection = self.totalSpeed*math.sin(self.angle)
        self.xball = self.xball+self.ballHDirection
        self.yball = self.yball+self.ballVDirection
        
        return reward1, reward2
        

    def draw(self, player_score, opponent_score):
        """Disegno del gioco"""
        self.window.fill((141,70,16))

        # punteggio racchetta sinistra
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(player_score), False, (255, 51, 51))
        self.window.blit(text_surface, (self.width/2 - 100, 16))

        # punteggio racchetta destra
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(opponent_score), False, (0, 204, 0))
        self.window.blit(text_surface, (self.width/2 + 100, 16))

        # disegno linea separazione per punteggio
        pygame.draw.line(self.window, (255, 255, 255), (0, 55), (self.width, 55), 5)
        pygame.draw.line(self.window, (255, 255, 255), (0, self.height-20), (self.width, self.height-20), 5)

        # disegno la palla
        pygame.draw.circle(self.window, (255, 255, 255),
                            (self.xball, self.yball), 5)
        # disegno racchetta sinistra
        pygame.draw.rect(self.window, (255, 51, 51),
                            (30, self.agent_1_position, 10, self.paddle_length))
        # disegno racchetta destra
        pygame.draw.rect(self.window, (0, 204, 0),
                            (self.width-40, self.agent_2_position, 10, self.paddle_length))
        # aggiorna il display
        pygame.display.flip()
