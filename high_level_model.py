import os
import pickle
from Util.State import State
from Util.Edge import Edge
from Util.Objective import Objective
from minigrid_env import Maze
from subtask_controller import SubtaskController
import networkx as nx
import matplotlib.pyplot as plt


class HLM:
    def __init__(self, objectives =None, start_state=None, goal_state=None, env_settings=None):
        self.env_settings = env_settings
        self.env = Maze(**env_settings)
        self.controllers = []
        self.objectives = objectives
        self.success_probabilities = []
        self.cost = []
        self.start_state = start_state
        self.goal_state = goal_state
        self.states = []
        self.edges = []


    def train_subcontrollers(self):
        '''
        Train subcontrollers for all objectives (sub-tasks) 
        and collect their statistics (cost and success probability)
        '''
        controller_id = 0
        print("start training " + str(len(self.objectives)) + " Controllers")
        for task in self.objectives:
            controller = SubtaskController(controller_id, task.start_state, task.final_state, env_settings=self.env_settings,
                 observation_top=task.observation_top, observation_width=task.observation_width, observation_height=task.observation_height)
            controller.learn(20000)
            self.controllers.append(controller)
            controller_id += 1
            print("controller" + str(controller_id) + " done")

    def save(self, save_dir):
        """
        Save the subcontrollers/HLM 
        """

        #Create path and folder to save HLM in
        save_path = os.path.join('Models', save_dir)
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        #Create subfolder to save subcontrollers of this HLM in
        subcontrollers_path = os.path.join('Models', save_dir, 'Subcontrollers')
        if not os.path.isdir(subcontrollers_path):
            os.mkdir(subcontrollers_path)

        #Save each subcontroller in a seperate folder
        for controller in self.controllers:
            controller_dir = "controller" + str(controller.id)
            controller_path = os.path.join(subcontrollers_path, controller_dir)
            controller.save(controller_path)

        #Save the data from the models
        model_file = os.path.join(save_path, 'model_data.p')
        model_data = {
            'objectives': self.objectives,
            'start_state': self.start_state,
            'goal_state': self.goal_state,
            'env_settings': self.env_settings
        }

        with open(model_file, 'wb') as pickleFile:
            pickle.dump(model_data, pickleFile)

    def load(self, load_dir):
        """
        Load the subcontrollers/HLM and create all edges and states in the model
        """


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
            S2 = State(name, task.final_state)
            
            if S2 not in self.states:
                self.states.append(S2)
                id += 1
            
        print('Done creating state of HLM')

    def find_edge_states(self, task):
        start_state = None
        end_state = None
        for state in self.states:
            if state.low_level_state == task.start_state:
                start_state = state

            if state.low_level_state == task.final_state:
                end_state = state
    
        return start_state, end_state 

    def find_controller(self, start_state, end_state):
        for controller in self.controllers:
            if controller.init_state == start_state and controller.final_state == end_state:
                return controller

    def create_edges(self):
        '''
        Create a edge for each controller between a start and final state
        '''
        print('Creating edges for HLM')

        id = 0
        for task in self.objectives:
            #find states regarding start and end of edge
            start_state, end_state = self.find_edge_states(task)

            #find controller regarding edge
            edge_controller = self.find_controller(start_state, end_state)

            #calculate probability and cost of edge
            edge_controller.eval_performance(n_episodes = 100)
            success_probability, cost, std = edge_controller.get_data()
            print(edge_controller.get_performance())

            #create edge
            id += 1
            name = 'E' + str(id)
            edge = Edge(name, edge_controller, start_state, end_state, success_probability, cost)
            #add edge to self.edges
            self.edges.append(edge)
        print('Done creating edges for HLM')

    def demonstrate_capabilities(self, n_episodes=8, n_steps=100, render=True):
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

            #reset environment
            self.env.set_observation_size(controller.observation_width, controller.observation_height, controller.observation_top)
            self.env.sub_task_goal = controller.final_state
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
                            #Goal reached
                            print(cur_edge.state2.to_string())
                            print(self.goal_state)
                            if cur_edge.state2 == self.goal_state:
                                print("goal reached! :)")
                                finished = True
                                break
                            #Find next controller
                            for edge in self.edges:
                                if edge.state1 == cur_edge.state2:
                                    controller = edge.controller
                                    self.env.set_observation_size(controller.observation_width, controller.observation_height, controller.observation_top)
                                    self.env.sub_task_goal = controller.final_state
                                    cur_edge = edge
                                    print("new controller = " + str(cur_edge.name))
                                    print("new controller start: " + str(cur_edge.state1.to_string()) + ", goal: " + str(cur_edge.state2.to_string()))
                                    obs = self.env.gen_obs()
                                    break
                        else:
                            print("sub task failed :(")
                            finished = True
                            break


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
        pos = nx.spectral_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size = 500)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=True)
        plt.show()
            


        



        

        