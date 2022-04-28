from sympy.logic.boolalg import to_cnf, Not
from typing import List

class World:
    values: str
    def __init__(self, values: str):
        self.values = values

    
#    def __init__(self, world):
#        self.world = world

class Worlds:
    worlds = List[World]

    def __init__(self):
        self.worlds = []

    def get_variables(self, belief_base, valid_operators):
        truth_list = []
        for key, value in belief_base.items():
            print("value formula", value.formula)
            for sub_str in value.formula:
                if sub_str not in valid_operators and sub_str.isalpha():
                    truth_list.append(sub_str)
        print("variables: ", list(set(truth_list)))
        return list(set(truth_list))

    def create_worlds(self, belief_combination, variables):

        self.worlds = []

        cnf_combinations = str(to_cnf(belief_combination, True))
        variable_count = len(variables)
        world_count = 2**variable_count
        temp_variables = variables[:]
        
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
            print(return_world.values)
            self.worlds.append(return_world)
            #print(self.worlds)
            #return self.worlds



        




    