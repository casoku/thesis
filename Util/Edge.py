class Edge:
    def __init__(self, name, controller, state1, state2, probability, cost):
        self.name = name
        self.controller = controller
        self.state1 = state1
        self.state2 = state2
        self.probability = probability
        self.cost = cost

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.state1 == other.state2 and self.state2 == other.state2

    def to_string(self):
        return str(self.name) + ", " + str(self.state1.name) + ", " + str(self.state2.name) + ", " + "{:.2f}".format(self.probability) + ", " + "{:.2f}".format(self.cost)