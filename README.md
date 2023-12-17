# Artificial Intelligence Ping-Pong

## How to Install

#### Requirements

- Python version 3.7+

#### Installation Steps

- Step 1: Download or clone the repository

- Step 2: Create a virtual enviroment

  - Run the command: python -m venv venv
  - Activate the virtual enviroment, run command: venv\Scripts\activate
  - Install dependencies, run command: pip install -r requirements.txt

- Step 3: Run the game
  - Run the command: python main.py   || you'll have a Q-learning agent on the left racket and a SARSA agent on the right racket
  - Run the command: python main.py -q   || you'll have a Q-learning agent on both racket
  - Run the command: python main.py -sarsa   || you'll have a SARSA agent on both racket
 
#### Train a model
- Step 1: Choose type of the model
  - Consider file learning_q_sarsa.py if you want train a model with a Q-learning agent and a SARSA agent
  - Consider file learning_q.py if you want train a model with two Q-learning agents
  - Consider file learning_sarsa.py if you want train a model with SARSA agents
 
- Step 2: Execute training of the model
  - In learning file you can setup hyper-parameters(alpha, gamma and epsilon values), game speed, number of episodes and other configurations
  - Execute your leaning file choosed in step 1, ex. run command: python learning_q_sarsa.py

- Step 3: Load your model and play the game
  - Run the command: python main.py   || if you choose learning_q_sarsa.py file
  - Run the command: python main.py -q   || if you choose learning_q.py file
  - Run the command: python main.py -sarsa   || if you choose learning_sarsa.py file
