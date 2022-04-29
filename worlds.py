from sympy.logic.boolalg import to_cnf, Not
from typing import List

class World:
    values: str
    def __init__(self, values: str):
        self.values = values

class Worlds:
    """k"""
    worlds = List[World]

    def __init__(self):
        self.worlds = []

    def get_variables(self, belief_base, valid_operators):
        """Get all variables included in the belief base at given time in their normal state"""
        truth_list = []
        for key, value in belief_base.items(): #implies != <> heldur = >>
            if "Implies" in value.formula: #p>>q = ~(Implies(p,q))
                temp = value.formula.replace("Implies", "") #okkur er alveg sama um <> í variables TODO strippa bara allt nema variables?
            else:
                temp = value.formula
            for sub_str in str(temp):                
               if sub_str not in valid_operators and sub_str.isalpha():
                   truth_list.append(sub_str)
        
        print("variables: ", list(set(truth_list)))
        return list(set(truth_list))

    def create_worlds(self, belief_combination, variables):
        """Create all possible worlds for the existing beliefs, the number of worlds generated
        is dependent on the number of variables n, world count = 2^n. The world creation is dependent 
        on the belief combination generated in beliefbase.py"""

        self.worlds = []  # list of possible worlds

        cnf_combinations = str(to_cnf(belief_combination, True)) 
        variable_count = len(variables) # define variable count
        world_count = 2**variable_count # generate number of worlds based on the variables
        temp_variables = variables[:] # empty list to store in iterations
        
        for i in range(world_count):
            new_world = cnf_combinations
            for k in range(variable_count):
                temp_variable = variables[k]
                if i % 2**(variable_count-k-1)==0 and i!=0:

                    if "~" in variables[k]:
                        variables[k] = variables[k].replace("~","")
                    else:
                        variables[k] = "~"+variables[k]
                
                new_world = new_world.replace(temp_variables[k], variables[k])
            new_world = new_world.replace("~~", "")
            return_world = World(new_world)
            #print(return_world.values)
            self.worlds.append(return_world)