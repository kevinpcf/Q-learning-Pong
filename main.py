import numpy as np
import joblib
from pongGame import pongGame

def load():
    """Funzione per caricare il modello salvato"""
    result = joblib.load("training.joblib")
        
    # Recupera la matrice Q
    return result['Q']

def normalize_x(val, width):
    ret = 0
    value = int(val)
    if(value < 41):
        ret = -10
    elif(value > width - 41):
        ret = -10
    elif(value <= width - 41):
        ret = value - 41
    return ret
        
def normalize_y( val, height):
    value = int(val) 
    if(value > height - 6):
        return -5
    elif(value < 5):
        return -5
    else: 
        return value - 5

def normalize_opponent( val):
    value = int(val / 5)
    return value - 1

def main():
    q_function = load()
    # Creare una maschera booleana per selezionare elementi con azione pari a 2
    mask = (q_function[:, :, :, :])

    # Ottenere gli indici in cui la maschera è vera
    indices = np.where(mask)

    # Stampa delle coordinate e dei valori corrispondenti
    for i in range(len(indices[0])):
        opponent_position = indices[0][i]
        xball = indices[1][i]
        yball = indices[2][i]
        action = indices[3][i]
        value = q_function[opponent_position, xball, yball, 2]

        # print(f"Coordinate: ({opponent_position}, {xball}, {yball}), Valore con azione 2: {value}")

    print("size", q_function.size)

    print("Inizio del gioco")
    num_episodes = 10
    for i in range(num_episodes):
        pong = pongGame()
        finish = False

        while not finish:
            _, opponent_position, xball, yball = pong.getState()
            
            opponent_position = normalize_opponent(opponent_position)

            xball = normalize_x(xball, pong.getWidth())
            yball = normalize_y(yball, pong.getHeight())

            action_values = q_function[opponent_position, xball, yball]
            action = np.argmax(action_values) 

            reward = pong.takeAction(action)   

            if reward == 100 or reward == -100:
                finish = True
            
            pong.draw()
    

if __name__ == "__main__":
    main()