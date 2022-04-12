class State:
    def __init__(self, name, low_level_state):
        self.name = name
        self.low_level_state = low_level_state
        self.edges = []

    def __eq__(self, other):
        if isinstance(other, State):
            return self.low_level_state == other.low_level_state
        else:
            return self.low_level_state[0] == other[0] and self.low_level_state[1] == other[1]

    def add_edge(self, e):
        self.edges.append(e)
    
    def to_string(self):
        return str(self.low_level_state)