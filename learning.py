from agent import Agent
from time import time
import numpy as np

def progress_bar(progress: float):
    """ Funzione per visualizzare il progresso del training """
    line = "["
    for _ in range(int(np.floor(progress * 25))):
        line += "="
    line += ">"

    for _ in range(26 - len(line)):
        line += " "
    line = line + "]" + str(int(np.floor(progress * 100))) + "%"
    print(line)

def main():
    agent = Agent(720, 576)
    num_episodes = 1000

    print("\nINZIO TRAINING")
    print("Progresso:\n")

    # Eseguo gli episodi e salvo nel training
    for i in range(num_episodes):
        # print(i)
        agent.run_learning_episode()
        progress_bar(float(i)/num_episodes)
        
        if(i == num_episodes-1):
            agent.save()

    progress_bar(1)

if __name__ == "__main__":
    main()