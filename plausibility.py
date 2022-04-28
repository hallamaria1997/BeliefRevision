from sympy.logic.boolalg import Not
from sympy.logic.boolalg import to_cnf
import itertools

class Worlds:
    def __init__(self):
        self.worlds = []

class Plausibility:
    def __init__(self):
        self.worlds = set()

    def plausibility_check(self, belief_base, valid_operators):
        truth_list = []
        for key, value in belief_base.items():
            for sub_str in value.formula:
                if sub_str not in valid_operators:
                    truth_list.append(sub_str)
        
        truth_list = set(truth_list)
        truth_sets = list(itertools.combinations(truth_list, int(len(truth_list)/2)))
        self.worlds = list(itertools.combinations(truth_list, int(len(truth_list)/2)))
        
        for a_tuple in truth_sets:
            for elem in a_tuple:
                matching = [s for s in a_tuple if elem in s]
                if len(matching) > 1:
                    self.worlds.remove(a_tuple)
                    break
        
        self.worlds = list(self.worlds)
        for i, a_tuple in enumerate(self.worlds):
            self.worlds[i] = ' & '.join(a_tuple)

        print(self.worlds)       
        return self.worlds

    def plausibility_order(self, belief_base ,belief):
        

        belief_combination = str(to_cnf('&'.join(
            [str(belief.cnf) for belief in belief_base.values()]), True))
        print('Belief combinations:',belief_combination)

        for indx, world in enumerate(self.worlds):
            print('world', world)
            print('BLC', belief_combination)
            if world == to_cnf(belief_combination):
                print('index, value;',indx, self.worlds[indx])











        #     statement_list = statement.split()
        #     for i, s in enumerate(statement_list):
        #         if s[0] == '~':
        #             statement_list[i] = 'False'
        #         if s[0].isalpha():
        #             statement_list[i] = 'True'

        # statement_str = ' '.join(statement_list)
        # belief_list = list(belief)
        # count = 0
        
        # while True:
            
        #     if count >= (len(belief_list)):
        #         break

        #     if belief_list[count] == '~':
        #         belief_list[count] = 'False'
        #         belief_list.pop(count+1)
        #         count += 1
            
        #     elif belief_list[count].isalpha():
        #        belief_list[count] = 'True'
        #        count += 1
            
        #     else:
        #         count += 1

        # print("belief list: ", belief_list)
        # print("statement list: ", statement_list)

        # belief_str = " ".join(belief_list)
        # statement_str = " ".join(statement_list)