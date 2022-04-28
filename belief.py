from sympy.logic.boolalg import to_cnf

class Belief:
    
    formula: str
    cnf: str
    priority: int

    def __init__(self, formula: str, priority: int):
        self.formula = formula
        self.cnf = to_cnf(formula)
        self.priority = priority

    def __repr__(self):
        return self.formula