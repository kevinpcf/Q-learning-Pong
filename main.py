import numpy as np
import joblib
from pongGame import pongGame
import sys, time

def load(filename):
    """Funzione per caricare il modello salvato"""
    result = joblib.load(filename)
        
    # Recupera la matrice Q
    return result['agent_1'], result['agent_2'], result['agent_1_score'], result['agent_2_score']

def normalize_x(val):
    """Funzione che mappa la coordinata x della palla nel corrispettivo stato"""
    # 1 stato corrisponde a 4 pixel dello schermo
    v = int(np.floor((val/400) * 100)) - 9
    if(v < 0):
        v = 0
    if (v >= 82):
        v = 82 - 1
    return v
        
def normalize_y(val):
    """Funzione che mappa la coordinata y della palla o della racchetta nel corrispettivo stato"""
    # 1 stato corrisponde a 4 pixel dello schermo
    v = int(np.floor((val/400) * 100)) - 15
    if(v < 0):
        v = 0
    if v >= 80:
        v = 80 - 1
    return v

def main():
    args = sys.argv[1:]
    if(len(args) == 1 and args[0] == "-q"):
        filename = "training_q_agents.joblib"
    elif(len(args) == 1 and args[0] == "-sarsa"):
        filename = "training_sarsa_agents.joblib"
    else:
        filename = "training_q_sarsa_agents.joblib"

    [agent_1, agent_2, agent_1_score, agent_2_score] = load(filename)

    # for y in range(agent_1.shape[0]):
    #     for x in range(agent_1.shape[1]):
    #         for ball_y in range(agent_1.shape[2]):
    #             for action in range(agent_1.shape[3]):
    #                 if(agent_1[y, x, ball_y, action] > 0):
    #                     print(f"Q({y}, {x}, {ball_y}, {action}): {agent_1[y, x, ball_y, action]}")

    print("Inizio del gioco")
    agent_1_score = 0
    agent_2_score = 0

    while (agent_1_score < 21 and agent_2_score < 21) :
        pong = pongGame()
        finish = False

        while not finish:
            agent_1_position, agent_2_position, xball, yball = pong.getState()
            
            agent_1_position = normalize_y(agent_1_position)
            agent_2_position = normalize_y(agent_2_position)
            xball = normalize_x(xball)
            yball = normalize_y(yball)

            action_values_1 = agent_1[agent_1_position, xball, yball]
            action_values_2 = agent_2[agent_2_position, xball, yball]
            action1 = np.argmax(action_values_1) 
            action2 = np.argmax(action_values_2) 

            reward1, reward2 = pong.takeAction(action1, action2)   

            if(reward1 == 8):
                agent_1_score = agent_1_score + 1
                finish = True
                time.sleep(0.2)
            elif(reward2 == 8):
                agent_2_score = agent_2_score + 1
                finish = True
                time.sleep(0.2)
            
            pong.draw(agent_1_score, agent_2_score)
    

if __name__ == "__main__":
    main()