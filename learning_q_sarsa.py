import numpy as np
import matplotlib
matplotlib.use('pdf')
import matplotlib.pyplot as plt
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
    window_height = 400
    window_width = 400
    num_episodes = 10000

    agent_1 = AgentQ(window_width, window_height, 0.6, 0.2, 0.5)
    agent_2 = AgentSarsa(window_width, window_height, 0.8, 0.1)

    print("\nINZIO TRAINING")
    print("Progresso:\n")

    rewardsum1 = 0
    rewardsum2 = 0
    rewards_avg1 = []
    rewards_avg2 = []
    durations_avg = []

    # eseguo gli episodi e salvo nel training
    for i in range(num_episodes):
    
        reward1sum, reward2sum, episode_duration = run_learning_episode_q_sarsa(agent_1, agent_2)
        rewardsum1 = rewardsum1 + reward1sum
        rewardsum2 = rewardsum2 + reward2sum
        
        if(i == num_episodes-1):
            save(agent_1, agent_2, rewards_avg1, rewards_avg2, durations_avg)
        if (i + 1) % 100 == 0:
            progress_bar(float(i)/num_episodes)
            agent_1.epsilon = max(agent_1.epsilon - 0.1, 0.1)
            print(f"Iterazione {i + 1}:")
            print("ricompensa 1 media", rewardsum1 / i)
            print("ricompensa 2 media", rewardsum2 / i)
            rewards_avg1.append(rewardsum1 / (i + 1))
            rewards_avg2.append(rewardsum2 / (i + 1))
            durations_avg.append(episode_duration)

    progress_bar(1)
    
    # mostra i risultati del modello ottenuto tramite dei grafici
    fig1, ax1 = plt.subplots(figsize=(21, 5))
    fig2, ax2 = plt.subplots(figsize=(21, 5))

    # Traccia il grafico delle ricompense medie
    ax1.plot(range(10, 100000 + 1, 10)[:len(rewards_avg1)], rewards_avg1, label='Agente 1')
    ax1.plot(range(10, 100000 + 1, 10)[:len(rewards_avg2)], rewards_avg2, label='Agente 2')
    ax1.set_xlabel('Episodio')
    ax1.set_ylabel('Ricompensa media')
    ax1.legend()

    # Traccia il grafico delle durate medie degli episodi
    ax2.plot(range(10, 100000 + 1, 10)[:len(durations_avg)], durations_avg, label='Durata media')
    ax2.set_xlabel('Episodio')
    ax2.set_ylabel('Durata media (secondi)')
    ax2.legend()

    # salva i grafici in formato PDF
    fig1.savefig('grafico_ricompense_learning_q_sarsa.pdf')
    fig2.savefig('grafico_durate_learning_q_sarsa.pdf')

    plt.close(fig1)
    plt.close(fig2)

if __name__ == "__main__":
    main()