import numpy as np
import random
from pongGame import pongGame
from agent import Agent, AgentQ, AgentSarsa
import joblib


def run_learning_episode_Q(agent_1: AgentQ, agent_2: AgentQ):
    pong = pongGame()
    function_Q_1 = agent_1.getQ()
    function_Q_2 = agent_2.getQ()

    finish = False

    while(not finish):
        # prendo gli stati della racchetta giocatore e le coordinate della palla 
        agent_1_position, agent_2_position, xball, yball = pong.getState()
        agent_1_position = agent_1.normalize_opponent(agent_1_position)
        agent_2_position = agent_2.normalize_opponent(agent_2_position)
        xball = agent_1.normalize_x(xball)
        yball = agent_1.normalize_y(yball)

        action_values1 = function_Q_1[agent_1_position, xball, yball]
        # scelgo un valore randomico
        random_greedy = random.random()
        # se il valore è maggiore di epsilon faccio exploitation
        if(random_greedy > agent_1.epsilon):
            action1 = np.argmax(action_values1)
        # altrimenti faccio exploration
        else:
            action1 = random.randint(0,2)

        action_values2 = function_Q_2[agent_2_position, xball, yball]
        # scelgo un valore randomico
        random_greedy = random.random()
        # se il valore è maggiore di epsilon faccio exploitation
        if(random_greedy > agent_1.epsilon):
            action2 = np.argmax(action_values2)
        # altrimenti faccio exploration
        else:
            action2 = random.randint(0,2)

        reward1, reward2 = pong.takeAction(action1, action2)

        # inizializzo i nuovi stati
        new_agent_1_position, new_agent_2_position, new_xball, new_yball = pong.getState()

        new_agent_1_position = agent_1.normalize_opponent(new_agent_1_position)
        new_agent_2_position = agent_2.normalize_opponent(new_agent_2_position)
        new_xball = agent_1.normalize_x(new_xball)
        new_yball = agent_1.normalize_y(new_yball)

        function_Q_1[agent_1_position, xball, yball, action1] = function_Q_1[agent_1_position, xball, yball, action1] + \
            agent_1.alpha * (reward1 + (agent_1.gamma * max(function_Q_1[new_agent_1_position, new_xball, new_yball])) - \
                function_Q_1[agent_1_position, xball, yball, action1])

        function_Q_2[agent_2_position, xball, yball, action2] = function_Q_2[agent_2_position, xball, yball, action2] + \
            agent_2.alpha * (reward2 + (agent_2.gamma * max(function_Q_2[new_agent_2_position, new_xball, new_yball])) - \
                function_Q_2[agent_2_position, xball, yball, action2])

        if(reward1 == 100):
            agent_1.score = agent_1.score + 1
            finish = True
        elif(reward2 == 100):
            agent_2.score = agent_2.score + 1
            finish = True

        pong.draw(agent_1.score, agent_2.score)

def run_learning_episode_sarsa(agent_1: AgentSarsa, agent_2: AgentSarsa):
    pong = pongGame()
    function_sarsa_1 = agent_1.getSarsa()
    function_sarsa_2 = agent_2.getSarsa()

    finish = False

    while(not finish):
        # prendo gli stati della racchetta giocatore e le coordinate della palla 
        agent_1_position, agent_2_position, xball, yball = pong.getState()
        agent_1_position = agent_1.normalize_opponent(agent_1_position)
        agent_2_position = agent_2.normalize_opponent(agent_2_position)
        xball = agent_1.normalize_x(xball)
        yball = agent_1.normalize_y(yball)
        
        action_values1 = function_sarsa_1[agent_1_position, xball, yball]
        action1 = np.argmax(action_values1)

        action_values2 = function_sarsa_2[agent_2_position, xball, yball]
        action2 = np.argmax(action_values2)

        reward1, reward2 = pong.takeAction(action1, action2)

        # inizializzo i nuovi stati
        new_agent_1_position, new_agent_2_position, new_xball, new_yball = pong.getState()

        new_agent_1_position = agent_1.normalize_opponent(new_agent_1_position)
        new_agent_2_position = agent_2.normalize_opponent(new_agent_2_position)
        new_xball = agent_1.normalize_x(new_xball)
        new_yball = agent_1.normalize_y(new_yball)

        function_sarsa_1[agent_1_position, xball, yball, action1] = function_sarsa_1[agent_1_position, xball, yball, action1] + \
            agent_1.alpha * (reward1 + (agent_1.gamma * function_sarsa_1[new_agent_1_position, new_xball, new_yball, action1]) - \
                function_sarsa_1[agent_1_position, xball, yball, action1])

        function_sarsa_2[agent_2_position, xball, yball, action2] = function_sarsa_2[agent_2_position, xball, yball, action2] + \
            agent_2.alpha * (reward2 + (agent_2.gamma * function_sarsa_2[new_agent_2_position, new_xball, new_yball, action2]) - \
                function_sarsa_2[agent_2_position, xball, yball, action2])

        if(reward1 == 100):
            agent_1.score = agent_1.score + 1
            finish = True
        elif(reward2 == 100):
            agent_2.score = agent_2.score + 1
            finish = True

        pong.draw(agent_1.score, agent_2.score)

def run_learning_episode_q_sarsa(agent_1: AgentQ, agent_2: AgentSarsa):
    pong = pongGame()
    function_Q_1 = agent_1.getQ()
    function_sarsa_2 = agent_2.getSarsa()

    finish = False

    while(not finish):
        # prendo gli stati della racchetta giocatore e le coordinate della palla 
        agent_1_position, agent_2_position, xball, yball = pong.getState()
        agent_1_position = agent_1.normalize_opponent(agent_1_position)
        agent_2_position = agent_2.normalize_opponent(agent_2_position)
        xball = agent_1.normalize_x(xball)
        yball = agent_1.normalize_y(yball)

        
        action_values1 = function_Q_1[agent_1_position, xball, yball]
        # scelgo un valore randomico
        random_greedy = random.random()
        # se il valore è maggiore di epsilon faccio exploitation
        if(random_greedy > agent_1.epsilon):
            action1 = np.argmax(action_values1)
        # altrimenti faccio exploration
        else:
            action1 = random.randint(0,2)

        action_values2 = function_sarsa_2[agent_2_position, xball, yball]
        action2 = np.argmax(action_values2)

        reward1, reward2 = pong.takeAction(action1, action2)

        # inizializzo i nuovi stati
        new_agent_1_position, new_agent_2_position, new_xball, new_yball = pong.getState()

        new_agent_1_position = agent_1.normalize_opponent(new_agent_1_position)
        new_agent_2_position = agent_2.normalize_opponent(new_agent_2_position)
        new_xball = agent_1.normalize_x(new_xball)
        new_yball = agent_1.normalize_y(new_yball)

        function_Q_1[agent_1_position, xball, yball, action1] = function_Q_1[agent_1_position, xball, yball, action1] + \
            agent_1.alpha * (reward1 + (agent_1.gamma * max(function_Q_1[new_agent_1_position, new_xball, new_yball])) - \
                function_Q_1[agent_1_position, xball, yball, action1])

        function_sarsa_2[agent_2_position, xball, yball, action2] = function_sarsa_2[agent_2_position, xball, yball, action2] + \
            agent_2.alpha * (reward2 + (agent_2.gamma * function_sarsa_2[new_agent_2_position, new_xball, new_yball, action2]) - \
                function_sarsa_2[agent_2_position, xball, yball, action2])

        if(reward1 == 100):
            agent_1.score = agent_1.score + 1
            finish = True
        elif(reward2 == 100):
            agent_2.score = agent_2.score + 1
            finish = True

        pong.draw(agent_1.score, agent_2.score)

def save(agent_1: Agent, agent_2: Agent):
    """ Funzione per salvare il modello """
    if(isinstance(agent_1, AgentQ)):
        function_1 = agent_1.getQ()
    else:
        function_1 = agent_1.getSarsa()

    if(isinstance(agent_2, AgentQ)):
        function_2 = agent_2.getQ()
    else:
        function_2 = agent_2.getSarsa()

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