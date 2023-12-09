import math
import random
import numpy as np
import pygame

class pongGame:

    def __init__(self):
        """ Inizializzazione dei parametri di gioco"""
        self.width = 720
        self.height = 576
        self.game_speed = 1

        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Ping Pong")

        # posizione x e y della palla
        self.xball = self.width/2
        self.yball = self.height/2

        # velocità della palla e angolazione
        direction = random.choice([0, 1])
        self.angle = random.random() * 0.5 * math.pi + 0.75 * math.pi
        if direction == 1:
            self.angle = random.random() * 0.25 * math.pi

        self.totalSpeed = self.game_speed
        self.ballHDirection = self.totalSpeed * math.cos(self.angle)
        self.ballVDirection = self.totalSpeed * math.sin(self.angle)

        # pozione delle racchette
        self.agent_1_position = self.height/2.4
        self.agent_2_position = self.height/2.4

        # lunghezza della racchetta
        self.paddle_length = self.height/6

    def getWidth(self): 
        return self.width

    def getHeight(self): 
        return self.height

    def getState(self):
        """Ritorna i valori degli stati (posizione della racchetta player,
        posizione della racchetta opponent, coordinata x della palla e coordinata y della palla)"""

        return np.array([self.agent_1_position, self.agent_2_position, self.xball, self.yball])

    def takeAction(self, action1, action2):
        reward1 = -1
        reward2 = -1
        
        # Movimento della racchetta del player
        if (action1 == 1 and self.agent_1_position >= 65) :
            self.agent_1_position = max(65, self.agent_1_position - 5)

            if (self.yball > self.agent_1_position \
            and self.yball < self.agent_1_position + self.paddle_length \
            and self.xball > 30 \
            and self.xball < 41):
                self.totalSpeed += 0.2
                self.angle = (
                    (math.pi / 4)
                    * (self.yball - (self.agent_1_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = 41
                reward1 = 10
        
        elif (action1 == 2 and self.agent_1_position < self.height - 5 - self.paddle_length) :
            self.agent_1_position = min(self.height - 5 - self.paddle_length, self.agent_1_position + 5)
            if (self.yball > self.agent_1_position \
            and self.yball < self.agent_1_position + self.paddle_length \
            and self.xball > 30 \
            and self.xball < 41):
                self.totalSpeed += 0.2
                self.angle = (
                    (math.pi / 4)
                    * (self.yball - (self.agent_1_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = 41
                reward1 = 10

        elif(action1 == 0):
            if(self.yball > self.agent_1_position \
            and self.yball < self.agent_1_position + self.paddle_length \
            and self.xball > 30 \
            and self.xball < 41):
                self.totalSpeed += 0.2
                self.angle = (
                    (math.pi / 4)
                    * (self.yball - (self.agent_1_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = 42
                reward1 = 10

        # Movimento della racchetta dell'opponent
        if (action2 == 1 and self.agent_2_position >= 65) :
            self.agent_2_position = max(65, self.agent_2_position - 5)

            if (self.yball > self.agent_2_position \
            and self.yball < self.agent_2_position + self.paddle_length \
            and self.xball > self.width - 41 \
            and self.xball < self.width - 30):
                self.totalSpeed += 0.2
                self.angle = (
                    math.pi
                    - (math.pi / 4)
                    * (self.yball - (self.agent_2_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = self.width - 41
                reward2 = 10
        
        elif (action2 == 2 and self.agent_2_position < self.height - 5 - self.paddle_length) :
            self.agent_2_position = min(self.height - 5 - self.paddle_length, self.agent_2_position + 5)
            if (self.yball > self.agent_2_position \
            and self.yball < self.agent_2_position + self.paddle_length \
            and self.xball > self.width - 41 \
            and self.xball < self.width - 30):
                self.totalSpeed += 0.2
                self.angle = (
                    math.pi
                    - (math.pi / 4)
                    * (self.yball - (self.agent_2_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = self.width - 41
                reward2 = 10

        elif(action2 == 0):
            if(self.yball > self.agent_2_position \
            and self.yball < self.agent_2_position + self.paddle_length \
            and self.xball > self.width - 41 \
            and self.xball < self.width - 30):
                self.totalSpeed += 0.2
                self.angle = (
                    math.pi
                    - (math.pi / 4)
                    * (self.yball - (self.agent_2_position + self.paddle_length / 2))
                    / (self.paddle_length / 2)
                )
                self.xball = self.width - 41
                reward2 = 10

        # se la palla è troppo a sinistra opponent ha vinto 
        if(self.xball < 41):
            reward1 = -100 
            reward2 = 100
        # se la palla è troppo a destra player ha vinto
        elif(self.xball > self.width - 41):
            reward1 = 100
            reward2 = -100

        # se la palla colpisce il bordo inferiore o superiore del gioco
        if(self.yball <= 65 or self.yball >= self.height - 5):
            self.angle = -self.angle

        self.ballHDirection = self.totalSpeed*math.cos(self.angle)
        self.ballVDirection = self.totalSpeed*math.sin(self.angle)
        self.xball = self.xball+self.ballHDirection
        self.yball = self.yball+self.ballVDirection
        
        return reward1, reward2
        
        
    def draw(self, player_score, opponent_score):
        """Disegno delle racchette e della pallina"""
        self.window.fill((141,70,16))

        # punteggio player
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(player_score), False, (255, 51, 51))
        self.window.blit(text_surface, (self.width/2 - 150, 16))

        # punteggio opponent
        font = pygame.font.Font(None, 50)
        text_surface = font.render(str(opponent_score), False, (0, 204, 0))
        self.window.blit(text_surface, (self.width/2 + 150, 16))

        # disegno linea per punteggio
        pygame.draw.line(self.window, (255, 255, 255), (0, 60), (self.width, 60), 5)
        pygame.draw.line(self.window, (255, 255, 255), (0, self.height-5), (self.width, self.height-5), 5)

        # disegno la palla
        pygame.draw.circle(self.window, (255, 255, 255),
                            (self.xball, self.yball), 5)
        # disegno player
        pygame.draw.rect(self.window, (255, 51, 51),
                            (31, self.agent_1_position, 10, self.paddle_length))
        # disegno opponent
        pygame.draw.rect(self.window, (0, 204, 0),
                            (self.width-41, self.agent_2_position, 10, self.paddle_length))
        # aggiorna il display
        pygame.display.flip()
