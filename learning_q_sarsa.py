from time import time
import numpy as np
from agent import AgentQ, AgentSarsa
from episode import run_learning_episode_q_sarsa, save


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
    window = 400
    num_episodes = 5000

    agent_1 = AgentQ(window, window, 0.6, 0.2, 0.5)
    agent_2 = AgentSarsa(window, window, 0.8, 0.1)

    print("\nINZIO TRAINING")
    print("Progresso:\n")

    rewardsum1 = 0
    rewardsum2 = 0

    # Eseguo gli episodi e salvo nel training
    for i in range(num_episodes):
    
        reward1sum, reward2sum = run_learning_episode_Q(agent_1, agent_2)
        rewardsum1 = rewardsum1 + reward1sum
        rewardsum2 = rewardsum2 + reward2sum
        
        if(i == num_episodes-1):
            save(agent_1, agent_2)
        if (i + 1) % 100 == 0:
            progress_bar(float(i)/num_episodes)
            agent_1.epsilon = max(agent_1.epsilon - 0.1, 0.1)
            print(agent_1.epsilon)
            print(f"Iterazione {i + 1}:")
            print("ricompensa 1 media", rewardsum1 / i)
            print("ricompensa 2 media", rewardsum2 / i)
    progress_bar(1)

if __name__ == "__main__":
    main()