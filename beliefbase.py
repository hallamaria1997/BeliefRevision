import re
from sympy.logic.boolalg import to_cnf, Not, Nor, Or, And, Equivalent
from belief import Belief
import itertools
from sympy.logic.inference import satisfiable
from itertools import product
from sympy import Q, symbols
from sympy.logic.boolalg import to_cnf
from sympy.logic import simplify_logic

class BeliefBase:
    cnf_format: str
    return_belief: str

    def __init__(self):
        self.beliefBase = {}
        self.valid_operators = ['&', '|', '>>', '<>', '~']

    def add(self, belief):
        if not self.validate_formatting(belief):
            print("Invalid formatting, press 'h' for help")
            return 0
        if not self.validate_belief(belief):
            print("invalid belief")
            return 0        

        self.revision(belief)

    def parsing_bicond(self, belief):
        """Formats biconditionality to match requirements 
            for sympy logic to_cnf"""
        bicond_patt = "<>"
        parenthesis_patt = '\((.+?)\)'
        belief = re.sub(bicond_patt, '>>', belief)
        belief = re.sub(r"[()]", "", belief)
        return_belief = '('+belief+')&('+belief[-1]+'>>'+belief[0]+')'
        return return_belief

    def to_belief(self,belief):
        belief = Belief(belief)
        return belief

    def get_belief_combinations(self, beliefBase):
        """Get all beliefs joined together using &"""
        belief_combination = str(to_cnf('&'.join(
            [str(belief.cnf) for belief in beliefBase.values()]), True))
        print('Belief combinations:',belief_combination)
        return belief_combination

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
                print(value.formula)
        return ''

    def validate_formatting(self, belief):
        """Validate format of user input"""
        self.operators = self.valid_operators[0:-1]
        # add whitespace between and split on space to create a list of inputs
        if " " not in belief:
            belief = " ".join(belief)
        belief = belief.split(" ")
        for i in range(len(belief)-1):
            if (not belief[i].isalpha() and not belief[i+1].isalpha) and (belief[i] not in self.valid_operators or belief[i]+belief[i+1] not in self.valid_operators):
                return False
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
        if (belief[0] in self.operators) or (belief[-1] in self.valid_operators):
            return False
    
        return True

    def validate_belief(self,belief):
        """Validate belief"""
        if "<>" in belief:
            belief = self.parsing_bicond(belief)

        if(not satisfiable(to_cnf(belief))):
            return False

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
            tempList = str(c).split("&")
            for t in tempList:
                cleaned_clauses.append(t.replace(" ", "").replace("(", "").replace(")", ""))

        clauses_cnf = cleaned_clauses

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

    #adds to the belief base without checking for consistency (is taken care of elsewhere)
    def expand(self, belief):
        """Adds to the belief base"""
        belief = Belief(belief)
        self.beliefBase[belief.formula] = belief

    #removes all beliefs that don't align with new belief
    def contract(self, negated_cnf, cnf):
        beliefBaseCopy = self.beliefBase.copy() #original beliefbase with all beliefs
        beliefBases = []

        if len(self.beliefBase) > 0:
            for key,item in beliefBaseCopy.items(): #traverses once
                beliefBaseOuterCopy = self.beliefBase.copy()
                self.beliefBase = beliefBaseOuterCopy
                for key1, item1 in beliefBaseCopy.items(): #traverses size of belief times
                    if(self.pl_resolution(negated_cnf)):
                        beliefBases.append(self.beliefBase.copy())
                    self.beliefBase.pop(key1, '')
                beliefBaseOuterCopy.pop(key, '')

        beliefsToRemove = min(beliefBases, key=len, default={})

        originalBeliefs = beliefBaseCopy
        self.beliefBase = self.remove_beliefs(originalBeliefs, beliefsToRemove)

    def remove_beliefs(self, originalBeliefs, beliefsToRemove):
        returnBase = originalBeliefs.copy()
        
        for key,item in originalBeliefs.items():
            for key1,item2 in beliefsToRemove.items():
                if key==key1:
                    returnBase.pop(key)

        return returnBase

    def revision(self, belief):
        """Changes existing beliefs in regards to new beliefs, uses """
        # Exclude all contradictions

        if "<>" in belief:
            belief = self.parsing_bicond(belief)

        cnf = to_cnf(belief)
        negated_cnf = to_cnf(f'~({cnf})')
        self.contract(negated_cnf, cnf)
        self.expand(belief)
        self.beliefBase.pop(str(negated_cnf), '')
