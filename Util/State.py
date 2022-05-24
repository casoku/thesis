from Util.martins_util import order_lexicographically


class State:
    def __init__(self, name, low_level_state, labels = []):
        self.name = name
        self.low_level_state = low_level_state
        self.edges = []
        self.labels = labels
        self.permanent_labels = []
        self.temporary_labels = []

    def __eq__(self, other):
        if isinstance(other, State):
            return self.low_level_state[0] == other.low_level_state[0] and self.low_level_state[1] == other.low_level_state[1]
        else:
            return self.low_level_state[0] == other[0] and self.low_level_state[1] == other[1]

    def add_edge(self, e):
        self.edges.append(e)

    def add_temporary_label(self, label):
        self.temporary_labels.append(label)
        order_lexicographically(self.temporary_labels)
    
    def add_permanent_label(self, label):
        self.permanent_labels.append(label)
        order_lexicographically(self.permanent_labels)


    def to_string(self):
        return "name: " +  self.name + ", low_level: " + str(self.low_level_state) + ", labels: " + str(self.labels)