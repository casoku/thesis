from numpy import Infinity


class Label:
    def __init__(self, probability=0, cost=0, predecessor=None, current=None, position = 0):
        self.probability = probability
        self.cost = cost
        self.permanent = False
        self.predecessor = predecessor
        self.current = current
        self.position = position

    def make_permanent(self):
        self.permanent = True
        self.current.temporary_labels.remove(self)
        self.current.permanent_labels.append(self)

    def dominate(self, other):
        if(self.probability > other.probability and self.cost < other.cost):
            return 1

        if(self.probability < other.probability and self.cost > other.cost):
            return -1

        return 0
    
    def state(self):
        return self.current

    # def __eq__(self, other):
    #     if isinstance(other, Label):
    #         return self.low_level_state == other.low_level_state

    def to_string(self):
        string = ""

        if(not self.permanent):
            string += '\033[91m'

        if(self.predecessor is None):
            pre_string = "None"
        else:
            pre_string = str(self.predecessor.name)

        if(self.current is None):
            cur_string = "None"
        else:
            cur_string = str(self.current.name)

        string += "(" + "{:.2f}".format(self.probability) + ", " + "{:.2f}".format(self.cost) + ", " + pre_string + ", " + cur_string + ", " + str(self.position) + ")"

        if(not self.permanent):
            string += '\033[0m'
        
        return string