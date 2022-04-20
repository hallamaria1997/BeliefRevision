import re
from sympy.logic.boolalg import to_cnf
import queue
from belief import Belief

#def add(self, belief):
#        """Adds belief from user input to the base"""
#        #add verification step
#        if '<>' in belief:
#            belief = self.parsing_bicond(belief)
#        self.cnf.append(to_cnf(belief))
#        self.beliefs.append(belief)


class BeliefBase:
    beliefBase : dict
    beliefCount : int
    return_belief: str

    def __init__(self):
        self.beliefBase = {}
        self.beliefCount = 0
        self.valid_operators = ['&', '|', '>>', '<>', '~']

    def add(self, belief):

        #add validate belief f.x. not q -> q shouldn't be let through
        #and there should not be any redundancies
        #if there are duplicates (thatis if we try to input something that's already in there)
        #I think we should remove it from the queue and add to the back of it so it becomes a higher priority
        #attention, should make sure A&B and B&A don't both exist
        if not self.validate_formatting(belief):
            return ("invalid formatting")
        if not self.validate_belief(belief):
            return ("invalid belief")
        
        belief = Belief(belief, self.beliefCount)
        #use pl resolution and if the sentence can be entailed from the BB
        #if is entailed from BB then expand right away
        if self.pl_resolution(self.beliefBase):
            self.expand(belief)
        else:
        #if isn't entailed
            #contract
            #expend
            self.contract(belief)
            self.expand(belief)

        return 1

    def parsing_bicond(self, belief):
        """Formats biconditionality to match requirements 
            for sympy logic to_cnf"""
        bicond_patt = "<>"
        parenthesis_patt = '\((.+?)\)'
        belief = re.sub(bicond_patt, '>>', belief)
        belief = re.sub(r"[()]", "", belief)
        return_belief = '('+belief+')&('+belief[-1]+'>>'+belief[0]+')'
        return return_belief


    def clear(self):
        """Clears all beliefs from the BeliefBase"""
        self.beliefs = {}

    def get(self):
        return list(self.beliefBase.values())

    def validate_formatting(self, belief):
        """Validate format of user input"""
        # add whitespace between and split on space to create a list of inputs
        if " " not in belief:
            belief = " ".join(belief)
        belief = belief.split(" ")
        # check if there is a digit
        if any(char.isdigit() for char in belief):
            return False
        # check if two consecutive characters and if two consecutive operators
        for i in range(0, len(belief) - 1):
            # check if they are not consecutive
            if (belief[i].isalpha() and belief[i+1].isalpha()):
                return False

            if (belief[i] in self.valid_operators) and (belief[i+1] in self.valid_operators):
                return False
        # check if operators are in the beginning or end of the string
        if (belief[0] in self.valid_operators) or (belief[-1] in self.valid_operators):
            return False
        return True

    def validate_belief(self,belief):
        """Validate belief, no contradictions"""
        if '<>' in belief:
            belief = self.parsing_bicond(belief)

        return True

    #let's do pl_resolution
    def pl_resolution(self, belief):
        return 1

    def expand(self, belief):
        self.beliefBase[belief.formula] = belief
        self.beliefCount += 1

    #not sure how we wanna do this, this is temporary, just removing right now
    def contract(self,belief):
        self.beliefBase.pop(belief.formula, None)

        #maybe here we create world and evaluate them
        #maybe from there we get a highest plausability order.... I'm not sure





