import copy
import os
import pickle
from xml import dom
import networkx as nx
import matplotlib.pyplot as plt
import random
from Util.Label import Label

from Util.State import State
from Util.Edge import Edge
from Util.high_level_model_util import *
from Util.martins_util import order_lexicographically
from subtask_controller import SubtaskController


class HLM:
    def __init__(self, objectives =None, start_state=None, goal_state=None, env=None, load_dir = None):
        self.controllers = []
        self.success_probabilities = []
        self.cost = []
        self.states = []
        self.edges = []

        if load_dir is None:
            self.env = copy.deepcopy(env)
            self.objectives = objectives
            self.start_state = start_state
            self.goal_state = goal_state
        else:
            self.load(load_dir)


    def train_subcontrollers(self):
        '''
        Train subcontrollers for all objectives (sub-tasks) 
        and collect their statistics (cost and success probability)
        '''
        controller_id = 0
        print("start training " + str(len(self.objectives)) + " Controllers")
        for task in self.objectives:
            controller = SubtaskController(controller_id, task.start_state, task.goal_state, env=self.env, verbose=0,
                 observation_top=task.observation_top, observation_width=task.observation_width, observation_height=task.observation_height)
            controller.learn(10000)
            self.controllers.append(controller)
            controller_id += 1
            print("controller" + str(controller_id) + " done")

    def save(self, save_dir):
        """
        Save the subcontrollers/HLM 
        """

        #Create locations and files to save to
        model_file, subcontroller_path = create_HLM_save_files(save_dir)

        #Save each subcontroller in a seperate folder
        for controller in self.controllers:
            controller_dir = "controller" + str(controller.id)
            controller_path = os.path.join(subcontroller_path, controller_dir)
            controller.save(controller_path, HLM_save = True)

        #Save the data from the models
        model_data = {
            'objectives': self.objectives,
            'start_state': self.start_state,
            'goal_state': self.goal_state,
            'env': self.env
        }

        with open(model_file, 'wb') as pickleFile:
            pickle.dump(model_data, pickleFile)

    def load(self, load_dir):
        """
        Load the subcontrollers/HLM and create all edges and states in the model
        """
        # Load model data
        load_path = os.path.join('Models', load_dir)
        model_file = os.path.join(load_path, 'model_data.p')
        with open(model_file, 'rb') as pickleFile:
            model_data = pickle.load(pickleFile)

        self.objectives = model_data['objectives']
        self.start_state = model_data['start_state']
        self.goal_state = model_data['goal_state']
        self.env = model_data['env']

        #Load subcontrollers
        controllers_path = os.path.join(load_path, 'Subcontrollers')
        for controller_file in next(os.walk(controllers_path))[1]:
            subtask_controller_path = os.path.join(controllers_path, controller_file)
            subtask_controller = SubtaskController(load_dir=subtask_controller_path, HLM_load=True)
            self.controllers.append(subtask_controller)

        #Create the edges and states for the loaded HLM
        self.create_states()
        self.create_edges()

    def create_states(self):
        '''
        States that are part of the high level model,
        Include all start and final states
        '''
        print('Creating state of HLM')
        id = 1
        for task in self.objectives:
            name = "S" + str(id)
            S1 = State(name, task.start_state)
            
            if S1 not in self.states:
                self.states.append(S1)
                id += 1
            
            name = "S" + str(id)
            S2 = State(name, task.goal_state)
            
            if S2 not in self.states:
                self.states.append(S2)
                id += 1
            
        print('Done creating state of HLM')

    def print_controllers_performance(self):
        for controller in self.controllers:
            print("controller id: " + str(controller.id) + ", start_state: " + str(controller.start_state) + ", goal_state: " + str(controller.goal_state))
            print(controller.get_performance())

    def create_edges(self):
        '''
        Create a edge for each controller between a start and final state
        '''
        print('Creating edges for HLM')

        id = 0
        for task in self.objectives:
            #find states regarding start and end of edge
            start_state, end_state = find_edge_states(self, task)

            #find controller regarding edge
            edge_controller = find_controller(self, start_state, end_state)

            #calculate probability and cost of edge
            edge_controller.eval_performance(n_episodes = 100)
            success_probability, cost, std = edge_controller.get_data()

            #create edge
            id += 1
            name = 'E' + str(id)
            edge = Edge(name, edge_controller, start_state, end_state, success_probability, cost)
            self.edges.append(edge)
            start_state.add_edge(edge)
        print('Done creating edges for HLM')

    def demonstrate_capabilities(self, n_episodes=8, n_steps=100, render=True):
        '''
        Dummy method, currently it just selects the first controller who's starting state is 
        equal to the finish of the previous task. Should use the higher level planning synthesized with planning
        '''
        for episodes in range(n_episodes):
            # select start controller
            controller = None
            cur_edge = None
            for edge in self.edges:
                if edge.state1 == self.start_state:
                    cur_edge = edge
                    controller = edge.controller
                    break
            print("Demonstrating capabilities")
            print("new controller = " + str(cur_edge.name))
            print("new controller start: " + str(cur_edge.state1.to_string()) + ", goal: " + str(cur_edge.state2.to_string()))
            #reset environment
            self.env.set_observation_size(controller.observation_width, controller.observation_height, controller.observation_top)
            self.env.sub_task_goal = controller.goal_state
            obs = self.env.reset()
            self.env.render(highlight=False)

            finished = False
            while not finished:
                for step in range(n_steps):
                    action, _states = controller.model.predict(obs, deterministic=True)
                    obs, reward, done, info = self.env.step(action)
                    if render:
                        self.env.render(highlight=False)
                    if done:
                        print(info)
                        if info['task_complete']:
                            print(cur_edge.state2.to_string())
                            print(self.goal_state)
                            #Goal reached
                            if cur_edge.state2 == self.goal_state:
                                print("goal reached! :)")
                                finished = True
                                break
                            #Find next possible controller
                            potentialControllers = []
                            for edge in self.edges:
                                if edge.state1 == cur_edge.state2:
                                    potentialControllers.append(edge)
                            
                            #Select next controller at random
                            edge = random.choice(potentialControllers)
                            controller = edge.controller
                            self.env.set_observation_size(controller.observation_width, controller.observation_height, controller.observation_top)
                            self.env.sub_task_goal = controller.goal_state
                            cur_edge = edge
                            print("new controller = " + str(cur_edge.name))
                            print("new controller start: " + str(cur_edge.state1.to_string()) + ", goal: " + str(cur_edge.state2.to_string()))
                            obs = self.env.gen_obs()

                        else:
                            print("sub task failed :(")
                            finished = True
                            break
    
    def martins_algorithm(self):
        print("TODO")
        temporary_labels = []

        #Set start label and make permanent
        cur_state = get_state(self, self.start_state)   
        label = Label(1, 0, None, cur_state, 0)
        cur_state.add_temporary_label(label)
        temporary_labels.append(label)

        while temporary_labels:
            temporary_labels = order_lexicographically(temporary_labels)

            print("------------------------------")
            for i in range(len(temporary_labels)):
                print(str(i) + ": " + temporary_labels[i].to_string())
            print("------------------------------")

            cur_label = temporary_labels[0]
            print("cur label:" + cur_label.to_string())
            print("cur state: " + cur_label.state().to_string())
            cur_label.make_permanent()
            temporary_labels.remove(cur_label)

            for edge in cur_label.state().edges:
                print(edge.to_string())
                probability = cur_label.probability * edge.probability
                cost = cur_label.cost + edge.cost
                predecessor = get_state(self, edge.state1)
                current = get_state(self, edge.state2)

                label = Label(probability, cost, predecessor, current, 0)
                print(label.to_string())
                #check if new label is dominated or not, if not add to temporary labels
                dominated = False
                for permanent_label in current.permanent_labels:
                    print(permanent_label.to_string())
                    if permanent_label.dominate(label) == 1:
                        dominated = True

                for temporary_label in current.temporary_labels:
                    if temporary_label.dominate(label) == 1:
                        dominated = True
                    
                    if temporary_label.dominate(label) == -1:
                        current.temporary_labels.remove(temporary_label)
                        temporary_labels.remove(temporary_label)

                print(dominated)

                if not dominated:
                    current.add_temporary_label(label)
                    temporary_labels.append(label)

                #add label to next edge node temporary labels

                
                #see which temporary labels can be deleted 

        #Print permanent labels of final node
        for label in get_state(self, self.goal_state).permanent_labels:
            print(label.to_string())


    def generate_graph(self):
        '''
        Generate a graph displaying the model
        '''

        G = nx.DiGraph()

        #generate edges
        graph_edges = []
        for edge in self.edges:
            graph_edge = (str(edge.state1.name), str(edge.state2.name))
            graph_edges.append(graph_edge)

        G.add_edges_from(
            graph_edges)

        # Specify the edges you want here
        black_edges = [edge for edge in G.edges()]

        # Need to create a layout when doing
        # separate calls to draw nodes and edges
        pos = nx.circular_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True, width=2)
        plt.show()
            


        



        

        