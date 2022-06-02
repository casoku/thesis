from matplotlib import pyplot as plt
from Util.State import State
from Util.Edge import Edge
import networkx as nx
import graphviz

class Graph:
    def __init__(self, states = [], start_state = None, final_states = [], edges = []):
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.edges = edges

        if start_state is None and len(states > 0):
            start_state = states[0]

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

    def is_final_state(self, state):
        for fs in self.final_states:
            if fs.name == state.name:
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

    def show_graph(self):
        f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
        f.attr(rankdir='LR', size='8,5')

        for state in self.states:
            if state.name == self.start_state.name:
                f.attr('node', shape='Mdiamond')
            elif self.is_final_state(state):
                print("hihi")
                f.attr('node', shape='doublecircle')
            else:
                f.attr('node', shape='circle')

            
            f.node(state.name)

        f.attr('node', shape='circle')
        for edge in self.edges:
            f.edge(edge.state1.name, edge.state2.name, label=str(edge.labels))

        f.view()
    

    