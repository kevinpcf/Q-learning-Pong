import numpy as np
import joblib
from pongGame import pongGame
import sys, time

def load(filename):
    """Funzione per caricare il modello salvato"""
    result = joblib.load(filename)
        
    # Recupera la matrice Q
    return result['agent_1'], result['agent_2'], result['agent_1_score'], result['agent_2_score']

def normalize_x(val, width):
    ret = 0
    value = int(val)
    if(value < 41):
        ret = 0
    elif(value > width - 41):
        ret = width - 81
    elif(value <= width - 41):
        ret = value - 41
    return ret
        
def normalize_y(val, height):
    value = int(val) 
    if(value > height - 6):
        return -5
    elif(value < 65):
        return -5
    else: 
        return value - 65

def normalize_opponent( val):
    value = int(val / 5)
    return value - 13

def main():
    args = sys.argv[1:]
    if(len(args) == 1 and args[0] == "-q"):
        filename = "training_q_agents.joblib"
    elif(len(args) == 1 and args[0] == "-sarsa"):
        filename = "training_sarsa_agents.joblib"
    else:
        filename = "training_q_sarsa_agents.joblib"

    [agent_1, agent_2, agent_1_score, agent_2_score] = load(filename)

    print("Inizio del gioco")
    agent_1_score = 0
    agent_2_score = 0

    while (agent_1_score < 21 and agent_2_score < 21) :
        pong = pongGame()
        finish = False

        while not finish:
            agent_1_position, agent_2_position, xball, yball = pong.getState()
            
            agent_1_position = normalize_opponent(agent_1_position)
            agent_2_position = normalize_opponent(agent_2_position)
            xball = normalize_x(xball, pong.getWidth())
            yball = normalize_y(yball, pong.getHeight())

            action_values_1 = agent_1[agent_1_position, xball, yball]
            action_values_2 = agent_2[agent_2_position, xball, yball]
            action1 = np.argmax(action_values_1) 
            action2 = np.argmax(action_values_2) 

            reward1, reward2 = pong.takeAction(action1, action2)   

            if(reward1 == 100):
                agent_1_score = agent_1_score + 1
                finish = True
                time.sleep(0.2)
            elif(reward2 == 100):
                agent_2_score = agent_2_score + 1
                finish = True
                time.sleep(0.2)
            
            pong.draw(agent_1_score, agent_2_score)
    

if __name__ == "__main__":
    main()