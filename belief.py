from sympy.logic.boolalg import to_cnf

class Belief:
    
    formula: str
    cnf: str

    def __init__(self, formula: str):
        self.formula = formula
        self.cnf = to_cnf(formula)

    def __repr__(self):
        return self.formula