import copy
from tkinter import font
from turtle import shape
from Util.Label import Label
from Util.State import State
from Util.Edge import Edge
import graphviz

from Util.martins_util import order_lexicographically

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

    def get_edge_by_states(self, start_state, end_state):
        for edge in self.edges:
            if edge.state1 == start_state and edge.state2 == end_state:
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
        #print(state.to_string())
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

    def martins_algorithm(self):
        #TODO write martins algorithm for a graph, so it can be generalized
        temporary_labels = []

        #Set start label and make permanent
        cur_state = self.get_state_by_name(self.start_state.name) 
        label = Label(1, 0, None, cur_state, 0)
        cur_state.add_temporary_label(label)
        temporary_labels.append(label)

        while temporary_labels:
            temporary_labels = order_lexicographically(temporary_labels)

            # print("------------------------------")
            # for i in range(len(temporary_labels)):
            #     print(str(i) + ": " + temporary_labels[i].to_string())
            # print("------------------------------")

            cur_label = temporary_labels[0]
            # print("cur label:" + cur_label.to_string())
            # print("cur state: " + cur_label.state().to_string())
            # print("cur edges:" + str(cur_label.state().outgoing_edges))
            cur_label.make_permanent()
            temporary_labels.remove(cur_label)

            for edge in cur_label.state().outgoing_edges:
                #print(edge.to_string())
                probability = round(cur_label.probability * edge.probability, 2)
                cost = cur_label.cost + edge.cost
                predecessor = edge.state1
                current = edge.state2
                #print("--" + str(predecessor.permanent_labels) + "--")
                position = len(predecessor.permanent_labels) - 1
                label = Label(probability, cost, predecessor, current, position)
                #print(label.to_string())
                #check if new label is dominated or not, if not add to temporary labels
                dominated = False
                for permanent_label in current.permanent_labels:
                    #print(permanent_label.to_string())
                    if permanent_label.dominate(label) == 1 or permanent_label.dominate(label) == 0:
                        dominated = True

                for temporary_label in current.temporary_labels:
                    if temporary_label.dominate(label) == 1:
                        dominated = True
                    
                    if temporary_label.dominate(label) == -1:
                        current.temporary_labels.remove(temporary_label)
                        temporary_labels.remove(temporary_label)

                #print(dominated)

                if not dominated:
                    current.add_temporary_label(label)
                    temporary_labels.append(label)

                #add label to next edge node temporary labels

                
                #see which temporary labels can be deleted 
        
        #print(self.goal_state)
        #Print permanent labels of final node
        for goal_state in self.final_states:
            for label in goal_state.permanent_labels:
                print(label.to_string())
    
    def find_optimal_paths_2(self):
        #find all labels of final states
        final_labels = []
        for state in self.states:
            for stateF in self.final_states:
                if state.name == stateF.name: 
                    for label in state.permanent_labels:
                        final_labels.append(label)
        
        # filter on pareto optimal labels in all final states
        temp = copy.deepcopy(final_labels)

        def dominate(dict1, other):
            if(dict1.probability == other.probability and dict1.cost == other.cost):
                return 0

            if(dict1.probability >= other.probability and dict1.cost <= other.cost):
                return 1

            if(dict1.probability <= other.probability and dict1.cost >= other.cost):
                return -1

            return 0

        for p1 in temp:
            for p2 in temp:
                if dominate(p2, p1) == 1:
                    for pp in final_labels:
                        if pp.probability == p1.probability and pp.cost == p1.cost:
                            final_labels.remove(pp)
                            break

        # find all paths according to labels             
        paths = []
        for label in final_labels:
            path = self.find_path(self.start_state.name, label, [label.current.name])
            path.reverse()

            edges = []
            for i in range(len(path)-1):
                edge = self.get_edge_by_states(self.get_state_by_name(path[i]), self.get_state_by_name(path[i + 1]))
                edges.append(edge)

            dict = {"edges": edges, "probability": label.probability, "cost": label.cost}
            paths.append(dict)

        return paths

    def find_path(self, start, label, pathI):
        pathI.append(label.predecessor.name)

        # path completed
        if(start == label.predecessor.name):
            return pathI

        return self.find_path(start, label.predecessor.permanent_labels[label.position], pathI)


    def find_optimal_paths(self):
        paths = []

        #Filter on unique labels in all states, to prevent duplicate paths
        filtered_states = {}
        for state in self.states:
            filtered_permanent_labels = []
            for label in state.permanent_labels:
                insert = True
                for filtered_label in filtered_permanent_labels:
                    if label.predecessor == filtered_label.predecessor:
                        insert = False
                
                if insert:
                    filtered_permanent_labels.append(label)
            
            filtered_states[str(state.name)] = filtered_permanent_labels
                
        print("---------------------------------------------------")
        for key in filtered_states:
            for item in filtered_states[key]:
                print(item.to_string())
        print("---------------------------------------------------")

        all_paths = []

        #return self.printAllPaths(self.start_state.name, self.final_states[0].name, filtered_states, paths)
        for stateF in self.final_states:
            tempPaths = self.findAllPaths(self.start_state.name, stateF.name, filtered_states, paths)
            for p in tempPaths:
                all_paths.append(p)

        def dominate(dict1, other):
            if(dict1["probability"] == other["probability"] and dict1["cost"] == other["cost"]):
                return 0

            if(dict1["probability"] >= other["probability"] and dict1["cost"] <= other["cost"]):
                return 1

            if(dict1["probability"] <= other["probability"] and dict1["cost"] >= other["cost"]):
                return -1

            return 0
        #filter out not pareto-optimal paths
        all_paths_copy = copy.deepcopy(all_paths)

        for p1 in all_paths_copy:
            for p2 in all_paths_copy:
                if dominate(p2, p1) == 1:
                    for pp in all_paths:
                        if pp["probability"] == p1["probability"] and pp["cost"] == p1["cost"]:
                            all_paths.remove(pp)
                            break
        
        b = []
        for i in range(len(all_paths)):
            if all_paths[i] not in all_paths[i+1:]:
                b.append(all_paths[i])

        # all_paths = b
        return all_paths, b
    
    #Prints all paths from 's' to 'd'

    def findAllPaths(self, s, d, filtered_states, paths):
 
        # Mark all the vertices as not visited
        visited ={}
        for state in self.states:
            visited[str(state.name)] = False
 
        # Create an array to store paths
        path = []
 
        print("start: " + s)
        print("destination: " + d)
        # Call the recursive helper function to print all paths
        self.findAllPathsUtil(d, s, visited, copy.deepcopy(path), filtered_states, paths)  

        return paths   

    def findAllPathsUtil(self, u, d, visited, path, filtered_states, paths):
 
        # Mark the current node as visited and store in path
        visited[u]= True
        path.append(u)
        # If current vertex is same as destination, then print
        # current path[]
        if u == d:
            path.reverse()
            #print(path)

            #find edges
            edges = []
            for i in range(len(path)-1):
                edge = self.get_edge_by_states(self.get_state_by_name(path[i]), self.get_state_by_name(path[i + 1]))
                edges.append(edge)
            
            #calculate total cost and probability per path
            probability = 1
            cost = 0

            for i in range(len(edges)):
                probability = round(probability * edges[i].probability, 2)
                cost += edges[i].cost

            insert = True
            for p in paths:
                if(p["probability"] >= probability and p["cost"] <= cost):
                    insert = False

            if insert:
                paths.append({"edges": edges, "probability": probability, "cost": cost})
            
            # for edge in edges:
            #     print(edge.to_string())

        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            #print(u)
            #print(filtered_states)
            for i in filtered_states[u]:
                #print(i.to_string())
                if i.predecessor.name in visited and visited[i.predecessor.name]== False:
                    self.findAllPathsUtil(i.predecessor.name, d, visited, copy.deepcopy(path),filtered_states, paths)
                     
        # Remove current vertex from path[] and mark it as unvisited
        path.pop()
        visited[u]= False
        
    def show_graph(self, name = 'fsm.gv'):
        f = graphviz.Digraph('finite_state_machine', filename='graphs/' + name)
        f.attr(rankdir='LR', size='8.5')
        #f.node("q1", shape="point")

        #print(self.states)
        for state in self.states:
            if state.name == self.start_state.name:
                f.attr('node', shape='Mdiamond', fontsize="24pt")
                #f.attr('node', shape='circle', fontsize="24pt")
                #f.edge("q1", self.start_state.name, fontsize="24pt")
            elif self.is_final_state(state):
                f.attr('node', shape='doublecircle', fontsize="24pt")
            else:
                f.attr('node', shape='circle', fontsize="24pt")

            
            f.node(state.name)

        f.attr('node', shape='circle')
        for edge in self.edges:
            f.edge(edge.state1.name, edge.state2.name, label=str(edge.labels), fontsize="24pt")

        f.view()
    

    