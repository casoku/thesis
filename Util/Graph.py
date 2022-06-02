from Util.State import State
from Util.Edge import Edge


class Graph:
    def __init__(self, states = [], edges = []):
        self.states = states
        self.edges = edges

    def get_edges(self):
        return self.edges

    def get_states(self):
        return self.states

    def get_state_by_name(self, name):
        for state in self.states:
            if state.name == name:
                return state

        return None

    def get_edge_by_name(self, name):
        for edge in self.edges:
            if edge.name == name:
                return edge

        return None

    def add_state(self, state):
        assert isinstance(state, State)

        self.states.append(state)

    def add_edge(self, edge):
        assert isinstance(edge, Edge)

        self.edges.append(edge)

    def contains_edge(self, edge):
        for e in self.edges:
            if e == edge:
                return True

        return False

    def contains_state(self, state):
        for s in self.states:
            if s == state:
                return True

        return False

    def remove_edge(self, edge):
        if self.contains_edge(edge):
            self.edges.remove(edge)
            return True

        return False

    def remove_state(self, state):
        if self.contains_state(state):
            self.states.remove(state)
            return True

        return False
    

    