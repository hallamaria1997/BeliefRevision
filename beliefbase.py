import re
from sympy.logic.boolalg import to_cnf, Not, Nor, Or, And, Equivalent
from belief import Belief
import itertools

class BeliefBase:
    cnf_format: str
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
            print("Invalid formatting, press 'h' for help")
            return 0
        if not self.validate_belief(belief):
            print("invalid belief")
            return 0
        
        belief = Belief(belief, self.beliefCount)
        #use pl resolution and if the sentence can be entailed from the BB

        #breyat þessu í eitt revision fall
        self.contract(belief)
        self.expand(belief)

        return 1

    def to_belief(self,belief):
        belief = Belief(belief, self.beliefCount)
        return belief

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
        self.beliefBase.clear()
        print("The Belief Base is now empty!")
        return ''

    def get(self):
        """Returns all beliefs in the base"""
        if len(self.beliefBase) == 0: print('There is nothing stored in the Belief Base!') 
        else:
            print("Overview of sentences in the Belief Base:\n")
            for value in self.beliefBase.values():
                print(value.cnf) #TODO breyta þessu til baka, fyrir test purposes
        return ''

    def validate_formatting(self, belief):
        """Validate format of user input"""
        self.operators = self.valid_operators[0:-1]
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

            if (belief[i] in self.valid_operators) and (belief[i+1] in self.operators):
                return False
        # check if operators are in the beginning or end of the string
        if (belief[0] in self.valid_operators) or (belief[-1] in self.valid_operators):
            return False
        return True

    def validate_belief(self,belief):
        """Validate belief, no contradictions"""
        if '<>' in belief:
            belief = self.parsing_bicond(belief)

        #TODO: add contradiction statement spotting
        #contradict = 

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

        not_alpha = to_cnf(Not(alpha))
        clauses_cnf = self.collect_beliefs_cnf()
        clauses_cnf.append(not_alpha)
        cleaned_clauses = []
        for c in clauses_cnf:
            #str(c).replace("(", "")
            #str(c).replace(")", "")
            tempList = str(c).split("&")
            for t in tempList:
                cleaned_clauses.append(t.replace(" ", "").replace("(", "").replace(")", ""))

        print("cleaned clauses: ", cleaned_clauses)

        clauses_cnf = cleaned_clauses

        #not_alpha = str(not_alpha).split("&")
        #print(not_alpha)
        #for n in not_alpha:
        #    print(n)
        #    clauses_cnf.append(n.replace(" ", "").replace("(", "").replace(")", ""))

        #clauses_cnf.append(not_alpha)
        #print(clauses_cnf)
        clause_pairs = self.get_clause_pairs(clauses_cnf)
        clauses = set(clauses_cnf)

        while True:
            new = set()
            clauses = set(clauses)
            clause_pairs = self.get_clause_pairs(clauses)

            for pairs in clause_pairs:
                resolvents = self.pl_resolve(pairs)
                if '' in resolvents: #if the list constains an empty clause
                    return True
                new = new.union(set(resolvents))

            if new.issubset(clauses):
                return False
            
            clauses = clauses.union(new)


    def pl_resolve(self,pairs):

        resolvents = []

        ci = str(pairs[0]).replace(" ", "").split("|")
        cj = str(pairs[1]).replace(" ", "").split("|")

        for i in ci:
            for j in cj:
                j_negate = str(Not(j))
                if i == j_negate:
                    temp_ci = ci
                    temp_cj = cj
                    [temp_ci.remove(i) for xi in temp_ci if xi == i]
                    [temp_cj.remove(j) for xj in temp_cj if xj == j]
                    temp_clause = temp_ci + temp_cj

                    temp_clause = list(set(temp_clause))
                    temp_clause = "|".join(temp_clause)
                    resolvents.append(temp_clause)
        
        return resolvents

    def expand(self, belief):
        #self.beliefBase[belief.formula] = belief
        self.beliefBase[self.beliefCount] = belief
        self.beliefCount += 1

    #not sure how we wanna do this, this is temporary, just removing right now
    #laga hverju við erum að poppa með, á að vera priority-ið frekar
    def contract(self,belief):
        self.beliefBase.pop(belief.formula, None)



        #maybe here we create world and evaluate them
        #maybe from there we get a highest plausability order.... I'm not sure

    def revision(self, belief):
        """Changes existing beliefs in regards to new beliefs"""
        # Exclude all contradictions
        contradicting_belief = Not(belief.cnf)

        if contradicting_belief in self.beliefs_cnf:
            self.contract(self.beliefs_cnf)
        
        self.expand(belief.formula)









