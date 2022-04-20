from agent import Agent
from belief import Belief

if __name__ == "__main__":
    agent = Agent()

    while agent.running:
        agent.get_action()

        