import numpy as np
import random
from pongGame import pongGame
from agent import Agent, AgentQ, AgentSarsa
import joblib

def run_learning_episode_Q(agent_1: AgentQ, agent_2: AgentQ):
    """Metodo che esegue un episodio di una partita q-learning vs q-learning"""
    pong = pongGame()
    finish = False
    reward1sum = 0
    reward2sum = 0
    i = 0

    while(not finish):
        i += 1
        # prendo i valori associati alle azioni nello stato corrente dell'agente 1
        action_values1 = agent_1.Q[agent_1_position, xball, yball]
        # scelgo un valore randomico
        random_greedy = random.random()
        # se il valore è maggiore di epsilon faccio exploitation
        if(random_greedy > agent_1.epsilon):
            action1 = np.argmax(action_values1)
        # altrimenti faccio exploration
        else:
            action1 = random.randint(0,2)

        # prendo i valori associati alle azioni nello stato corrente dell'agente 2
        action_values2 = agent_2.Q[agent_2_position, xball, yball]
        # scelgo un valore randomico
        random_greedy = random.random()
        # se il valore è maggiore di epsilon faccio exploitation
        if(random_greedy > agent_2.epsilon):
            action2 = np.argmax(action_values2)
        # altrimenti faccio exploration
        else:
            action2 = random.randint(0,2)

        # eseguo l'azione dell'agente 1 e 2 ed ottengo le ricompense
        reward1, reward2 = pong.takeAction(action1, action2)

        # prendo le nuove posizioni della racchetta sinistra, della racchetta destra e le coordinate x e y della palla 
        new_agent_1_position, new_agent_2_position, new_xball, new_yball = pong.getState()

        # associo le coordinate ai rispettivi stati
        new_agent_1_position = agent_1.normalize_y(new_agent_1_position)
        new_agent_2_position = agent_2.normalize_y(new_agent_2_position)
        new_xball = agent_1.normalize_x(new_xball)
        new_yball = agent_1.normalize_y(new_yball)

        if((new_xball == xball + 1 or new_xball == xball -1) or (new_yball == yball + 1 or new_yball == yball -1)):
            # aggiorno la Q function dell'agente 1
            agent_1.Q[agent_1_position, xball, yball, action1] = agent_1.Q[agent_1_position, xball, yball, action1] + \
            agent_1.alpha * (reward1 + (agent_1.gamma * np.max(agent_1.Q[new_agent_1_position, new_xball, new_yball, :], axis = -1)) - \
                agent_1.Q[agent_1_position, xball, yball, action1])
        
            # aggiorno la Q function dell'agente 2
            agent_2.Q[agent_2_position, xball, yball, action2] = agent_2.Q[agent_2_position, xball, yball, action2] + \
            agent_2.alpha * (reward2 + (agent_2.gamma * np.max(agent_2.Q[new_agent_2_position, new_xball, new_yball, :], axis = -1)) - \
                agent_2.Q[agent_2_position, xball, yball, action2])
 
        reward1sum = reward1sum + reward1
        reward2sum = reward2sum + reward2

        # aggiorno gli stati
        agent_1_position = new_agent_1_position
        agent_2_position = new_agent_2_position
        xball = new_xball
        yball = new_yball

        # se l'episodio è finito assegno i punteggi
        if(reward1 == 8):
            agent_1.score = agent_1.score + 1
            finish = True
        elif(reward2 == 8):
            agent_2.score = agent_2.score + 1
            finish = True

        pong.draw(agent_1.score, agent_2.score)

    return reward1sum / i, reward2sum / i 

def run_learning_episode_sarsa(agent_1: AgentSarsa, agent_2: AgentSarsa):
    """Metodo che esegue un episodio di una partita sarsa vs sarsa"""
    pong = pongGame()
    reward1sum = 0
    reward2sum = 0
    i = 0

    # prendo le posizioni della racchetta sinistra, della racchetta destra e le coordinate x e y della palla
    agent_1_position, agent_2_position, xball, yball = pong.getState()

    # associo le coordinate ai rispettivi stati
    agent_1_position = agent_1.normalize_y(agent_1_position)
    agent_2_position = agent_2.normalize_y(agent_2_position)
    xball = agent_1.normalize_x(xball)
    yball = agent_1.normalize_y(yball)

    finish = False

    while(not finish):
        i += 1
        # prendo i valori associati alle azioni nello stato corrente dell'agente 1
        action_values1 = agent_1.sarsa[agent_1_position, xball, yball]

        # prendo l'azione da eseguire che il valore più alto
        action1 = np.argmax(action_values1)

        # prendo i valori associati alle azioni nello stato corrente dell'agente 2
        action_values2 = agent_2.sarsa[agent_2_position, xball, yball]

        # prendo l'azione da eseguire che il valore più alto
        action2 = np.argmax(action_values2)

        # eseguo l'azione dell'agente 1 e 2 ed ottengo le ricompense
        reward1, reward2 = pong.takeAction(action1, action2)

        # prendo le nuove posizioni della racchetta sinistra, della racchetta destra e le coordinate x e y della palla 
        new_agent_1_position, new_agent_2_position, new_xball, new_yball = pong.getState()

        # associo le coordinate ai rispettivi stati
        new_agent_1_position = agent_1.normalize_y(new_agent_1_position)
        new_agent_2_position = agent_2.normalize_y(new_agent_2_position)
        new_xball = agent_1.normalize_x(new_xball)
        new_yball = agent_1.normalize_y(new_yball)

        if((new_xball == xball + 1 or new_xball == xball -1) or (new_yball == yball + 1 or new_yball == yball -1)):
            # aggiorno la funzione sarsa dell'agente 1
            agent_1.sarsa[agent_1_position, xball, yball, action1] = agent_1.sarsa[agent_1_position, xball, yball, action1] + \
                agent_1.alpha * (reward1 + (agent_1.gamma * agent_1.sarsa[new_agent_1_position, new_xball, new_yball, action1]) - \
                    agent_1.sarsa[agent_1_position, xball, yball, action1])

            # aggiorno la funzione sarsa dell'agente 2
            agent_2.sarsa[agent_2_position, xball, yball, action2] = agent_2.sarsa[agent_2_position, xball, yball, action2] + \
                agent_2.alpha * (reward2 + (agent_2.gamma * agent_2.sarsa[new_agent_2_position, new_xball, new_yball, action2]) - \
                    agent_2.sarsa[agent_2_position, xball, yball, action2])
    
        reward1sum = reward1sum + reward1
        reward2sum = reward2sum + reward2

        # aggiorno gli stati
        agent_1_position = new_agent_1_position
        agent_2_position = new_agent_2_position
        xball = new_xball
        yball = new_yball
        
        # se l'episodio è finito assegno i punteggi
        if(reward1 == 8):
            agent_1.score = agent_1.score + 1
            finish = True
        elif(reward2 == 8):
            agent_2.score = agent_2.score + 1
            finish = True

        pong.draw(agent_1.score, agent_2.score)
    
    return reward1sum / i, reward2sum / i 

def run_learning_episode_q_sarsa(agent_1: AgentQ, agent_2: AgentSarsa):
    """Metodo che esegue un episodio di una partita q_learning vs sarsa"""
    pong = pongGame()
    reward1sum = 0
    reward2sum = 0
    i = 0

    # prendo le posizioni della racchetta sinistra, della racchetta destra e le coordinate x e y della palla 
    agent_1_position, agent_2_position, xball, yball = pong.getState()

    # associo le coordinate ai rispettivi stati
    agent_1_position = agent_1.normalize_y(agent_1_position)
    agent_2_position = agent_2.normalize_y(agent_2_position)
    xball = agent_1.normalize_x(xball)
    yball = agent_1.normalize_y(yball)

    finish = False

    while(not finish):
        # prendo i valori associati alle azioni nello stato corrente dell'agente 1
        action_values1 = agent_1.Q[agent_1_position, xball, yball]
        # scelgo un valore randomico
        random_greedy = random.random()
        # se il valore è maggiore di epsilon faccio exploitation
        if(random_greedy > agent_1.epsilon):
            action1 = np.argmax(action_values1)
        # altrimenti faccio exploration
        else:
            action1 = random.randint(0,2)

        # prendo i valori associati alle azioni nello stato corrente dell'agente 2
        action_values2 = agent_2.sarsa[agent_2_position, xball, yball]

        # prendo l'azione da eseguire che il valore più alto
        action2 = np.argmax(action_values2)

        # eseguo l'azione dell'agente 1 e 2 ed ottengo le ricompense
        reward1, reward2 = pong.takeAction(action1, action2)

        # prendo le nuove posizioni della racchetta sinistra, della racchetta destra e le coordinate x e y della palla 
        new_agent_1_position, new_agent_2_position, new_xball, new_yball = pong.getState()

        # associo le coordinate ai rispettivi stati
        new_agent_1_position = agent_1.normalize_y(new_agent_1_position)
        new_agent_2_position = agent_2.normalize_y(new_agent_2_position)
        new_xball = agent_1.normalize_x(new_xball)
        new_yball = agent_1.normalize_y(new_yball)

        # aggiorno la Q function dell'agente 1
        agent_1.Q[agent_1_position, xball, yball, action1] = agent_1.Q[agent_1_position, xball, yball, action1] + \
            agent_1.alpha * (reward1 + (agent_1.gamma * np.max(agent_1.Q[new_agent_1_position, new_xball, new_yball, :], axis = -1)) - \
                agent_1.Q[agent_1_position, xball, yball, action1])

        # aggiorno la funzione sarsa dell'agente 2
        agent_2.sarsa[agent_2_position, xball, yball, action2] = agent_2.sarsa[agent_2_position, xball, yball, action2] + \
            agent_2.alpha * (reward2 + (agent_2.gamma * agent_2.sarsa[new_agent_2_position, new_xball, new_yball, action2]) - \
                agent_2.sarsa[agent_2_position, xball, yball, action2])

        reward1sum = reward1sum + reward1
        reward2sum = reward2sum + reward2

        # aggiorno gli stati
        agent_1_position = new_agent_1_position
        agent_2_position = new_agent_2_position
        xball = new_xball
        yball = new_yball

        # se l'episodio è finito assegno i punteggi
        if(reward1 == 8):
            agent_1.score = agent_1.score + 1
            finish = True
        elif(reward2 == 8):
            agent_2.score = agent_2.score + 1
            finish = True

        pong.draw(agent_1.score, agent_2.score)
    return reward1sum / i, reward2sum / i

def save(agent_1: Agent, agent_2: Agent):
    """Funzione per salvare il modello"""
    if(isinstance(agent_1, AgentQ)):
        function_1 = agent_1.Q
    elif(isinstance(agent_1, AgentSarsa)):
        function_1 = agent_1.sarsa

    if(isinstance(agent_2, AgentQ)):
        function_2 = agent_2.Q
    elif(isinstance(agent_2, AgentSarsa)):
        function_2 = agent_2.sarsa

    result = {'agent_1': function_1, 'agent_2': function_2, 'agent_1_score': agent_1.score, 'agent_2_score': agent_2.score}
    # Salva come file joblib con compressione
    if((isinstance(agent_1, AgentQ) and isinstance(agent_2, AgentQ))):
        filename = "training_q_agents.joblib"
    elif((isinstance(agent_1, AgentSarsa) and isinstance(agent_2, AgentSarsa))):
        filename = "training_sarsa_agents.joblib"
    else:
        filename = "training_q_sarsa_agents.joblib"
    joblib.dump(result, filename, compress=('zlib', 3))
    print("File salvato correttamente")