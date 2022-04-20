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
        self.beliefBase = {}

    def get(self):
        return list(self.beliefBase.values())

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

