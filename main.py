from agent import Agent

if __name__ == "__main__":
    agent = Agent()

    while agent.running:
        agent.get_action()
        