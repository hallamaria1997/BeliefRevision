from beliefbase import BeliefBase

class Agent:
    def __init__(self):
        self.running = True
        self.belief_base = BeliefBase()
        print("User Guidelines:  When inserting your sentances to the belief base \nmake sure that they are correctly formatted.\n")
        print("Each sentanece can only contain single letters, operators and the words True/False")
        print("This setup uses the following operator translations: \n")
        print("Operator        | Syntax\nNegotion(NOT)   | ~\nConjuction(AND) | &\nDisjunction(OR) | |\nImplication     | >>\nBiconditional   | <>")
        #print("Negotion(NOT): ~p\nConjuction(AND): p&q\nDisjunction(OR): p|q\nImplication: p>>q\nBiconditional: p<>q\n")
        print("Finally, all sentances require parenthesis to indicate operator procedence: (p>>q)&p\n")

    def get_action(self):

        print("What do you wanna do??\n 1. Display belief base \n 2. Add to belief base \n 3. Clear belief base \n 4. Quit \n 5. check if BB entails your sentence")
        
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
        elif(action == "5"):
            self.belief_base.pl_resolution(belief)

    def quit(self):
        self.running = False

    def print_user_guides():
        print("User Guidelines:  ! = not, and = &, or -> = implies, <-> = if and only if, T=true, F = false. Use only lower case letters for connectives. Use ( ) to XXX")

