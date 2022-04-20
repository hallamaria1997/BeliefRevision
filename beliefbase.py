<<<<<<< HEAD
import re
from sympy.logic.boolalg import to_cnf

class BeliefBase:
    cnf_format: str
    return_belief: str

    def __init__(self, name=None, board=None):
        #TODO check if needs to be some other structure
        self.beliefs = []
        self.cnf = []
        print("calling belief base ")

    def add(self, belief):
        """Adds belief from user input to the base"""
        #add verification step
        if '<>' in belief:
            belief = self.parsing_bicond(belief)
        self.cnf.append(to_cnf(belief))
        self.beliefs.append(belief)
=======
import queue
from belief import Belief

class BeliefBase:
    beliefBase : dict
    beliefCount : int

    def __init__(self):
        self.beliefBase = {}
        self.beliefCount = 0

    def add(self, belief):
        belief = Belief(belief, self.beliefCount)

        #add validate formatting
        if not self.validate_formatting(belief):
            return ("descriptive text why didn't add")
        #add validate belief f.x. not q -> q shouldn't be let through
        #and there should not be any redundancies
        #if there are duplicates (thatis if we try to input something that's already in there)
        #I think we should remove it from the queue and add to the back of it so it becomes a higher priority
        #attention, should make sure A&B and B&A don't both exist
        if not self.validate_belief(belief):
            return ("descriptive text why didn't add")
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
>>>>>>> 7cd216a62ea6ec5e4431b53e081b486b2d38bbb6

    

    def parsing_bicond(self, belief):
        """Formats biconditionality to match requirements 
            for sympy logic to_cnf"""
        bicond_patt = "<>"
        parenthesis_patt = '\((.+?)\)'
        belief = re.sub(bicond_patt, '>>', belief)
        belief = re.sub(r"[()]", "", belief)
        return_belief = '('+belief+')&('+belief[3]+'>>'+belief[0]+')'

        return return_belief


    def clear(self):
<<<<<<< HEAD
        """Clears all beliefs from the BeliefBase"""
        self.beliefs = []

    def get(self):
        """Returns all beliefs in the base"""
        return self.beliefs
=======
        self.beliefBase = {}

    def get(self):
        return list(self.beliefBase.values())
>>>>>>> 7cd216a62ea6ec5e4431b53e081b486b2d38bbb6

    def validate_formatting(self, belief):
        return True

    def validate_belief(self,belief):
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

