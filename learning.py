from agent import Agent

def main():
    agent = Agent(768, 1024)

    for i in range(10000):
        agent.run_learning_episode()


if __name__ == "__main__":
    main()