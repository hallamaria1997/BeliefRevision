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
        """Clears all beliefs from the BeliefBase"""
        self.beliefs = []

    def get(self):
        """Returns all beliefs in the base"""
        return self.beliefs

    def validate_formatting(self, belief):
        len = len(belief)

    def validate_belief(self,belief):
        len = len(belief)

