from beliefbase import BeliefBase

class Agent:
    def __init__(self, name=None, board=None):
        self.running = True
        self.belief_base = BeliefBase()
        print("User Guidelines:  ! = not, and = &, or -> = implies, <-> = if and only if, T=true, F = false. Use only lower case letters for connectives. Use ( ) to XXX")

    def get_action(self):
        #add clear and quit
        print("What do you wanna do??\n 1. Display belief base \n 2. Add to belief base \n 3. Clear belief base \n 4. Quit")
        action = input() 

        if(action == "1"):
            print(self.belief_base.get())
        elif(action == "2"):
            belief = input("Input belief ")
            self.belief_base.add(belief)
        elif(action == "3"):
            self.belief_base.clear()
        elif(action == "4"):
            self.quit()

    def quit(self):
        self.running = False
