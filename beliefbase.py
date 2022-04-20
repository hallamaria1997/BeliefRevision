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
        return_belief = '('+belief+')&('+belief[3]+'>>'+belief[0]+')'

        return return_belief


    def clear(self):
        """Clears all beliefs from the BeliefBase"""
        self.beliefs = []

    def get(self):
        """Returns all beliefs in the base"""
        return self.beliefs

    def validate_formatting(self, belief):
        # check if there is a digit
        if any(char.isdigit() for char in belief):
            print("in here")
            return False
        # check if two consecutive characters

        # check if two consecutive operators
        return True

    def validate_belief(self,belief):
        """Validate belief, no contradictions"""
        if '<>' in belief:
            belief = self.parsing_bicond(belief)

        return True

    def collect_beliefs_cnf(self):
        beliefs_cnf = []
        for key,values in self.beliefBase.items():
            beliefs_cnf.append(values.cnf)
        return beliefs_cnf

    def get_clause_pairs(self, clauses):
        return list(itertools.combinations(clauses, 2))


    #based on PL-Resolution Algorithm from Aritifical Intelligence a modern approach p.255
    def pl_resolution(self, alpha):
        """Check if Beliefbase entails new belies"""

        not_alpha = Not(alpha.cnf)
        clauses_cnf = self.collect_beliefs_cnf().append(not_alpha)
        clause_pairs = self.get_clause_pairs(clauses_cnf)
        new = set()
        clauses = set(clauses_cnf)

        while True:
            for pairs in clause_pairs:
                resolvents = pl_resolve(pairs)
                if not resolvents: #if the list is empty
                    return True
                new = new.union(set(resolvents))
                
            if new.issubset(clauses):
                return False
            
            clauses = clauses.union(new)

    #ATH temporary
    def pl_resolve(self,pairs):
        return []

    def expand(self, belief):
        self.beliefBase[belief.formula] = belief
        self.beliefCount += 1

    #not sure how we wanna do this, this is temporary, just removing right now
    def contract(self,belief):
        self.beliefBase.pop(belief.formula, None)

        #maybe here we create world and evaluate them
        #maybe from there we get a highest plausability order.... I'm not sure





