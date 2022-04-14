
class BeliefBase:
    def __init__(self, name=None, board=None):
        #TODO check if needs to be some other structure
        self.beliefs = []
        print("calling belief base ")

    def add(self, belief):
        #add verification step
        self.beliefs.append(belief)

    def clear(self):
        self.beliefs = []

    def get(self):
        return self.beliefs

    def validate_formatting(self, belief):
        len = len(belief)

    def validate_belief(self,belief):
        len = len(belief)

