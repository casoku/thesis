import copy
import os
import pickle
import spot
import numpy as np

from Util.Graph import Graph
from Util.State import State
from Util.Edge import Edge
from Util.automata_util import LTL_to_automata, solve_edge_bool_expression
from Util.high_level_model_util import *
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
            print(task.to_string())
            controller = SubtaskController(controller_id, task.start_state, task.goal_state, env=self.env, verbose=0,
                 observation_top=task.observation_top, observation_width=task.observation_width, observation_height=task.observation_height)
            controller.learn(50000)
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
            S1 = State(name, task.start_state, task.labels)
            
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
            edge = Edge(name, edge_controller, start_state, end_state, success_probability, cost, task.labels)
            self.edges.append(edge)
            start_state.add_outgoing_edge(edge)
            end_state.add_incoming_edge(edge)
        print('Done creating edges for HLM')

    def demonstrate_HLC(self, path, n_episodes=8, n_steps=100, render=True):
        '''
        Demonstrates a planning in the environment, the path exist out of subtask to executes in which order (left to right)
        '''
        total_cost = []
        total_successes = []

        for episodes in range(n_episodes):
            cost = 0

            # select start controller
            cur_edge = path["edges"][0]
            controller = cur_edge.controller
            print("Demonstrating capabilities")
            #print("new controller = " + str(cur_edge.name))
            #print("new controller start: " + str(cur_edge.state1.to_string()) + ", goal: " + str(cur_edge.state2.to_string()))
            #reset environment
            self.env.set_observation_size(controller.observation_width, controller.observation_height, controller.observation_top)
            self.env.sub_task_goal = controller.goal_state
            obs = self.env.reset()
            if render:
                self.env.render(highlight=False)

            next_edge_index = 1
            finished = False
            while not finished:
                for step in range(n_steps):
                    action, _states = controller.model.predict(obs, deterministic=True)
                    obs, reward, done, info = self.env.step(action)
                    cost += 1
                    if render:
                        self.env.render(highlight=False)
                    if done:
                        #print(info)
                        if info['task_complete']:
                            #print(cur_edge.state2.to_string())
                            #print(self.goal_state)
                            #Goal reached
                            if cur_edge.state2.name == path["edges"][-1].state2.name:
                                print("goal reached! :)")
                                finished = True
                                total_cost.append(cost)
                                total_successes.append(1)
                                break
                            
                            #Select next controller and reset environment
                            edge = path["edges"][next_edge_index]
                            controller = edge.controller
                            self.env.set_observation_size(controller.observation_width, controller.observation_height, controller.observation_top)
                            self.env.sub_task_goal = controller.goal_state
                            cur_edge = edge
                            next_edge_index += 1
                            #print("new controller = " + str(cur_edge.name))
                            #print("new controller start: " + str(cur_edge.state1.to_string()) + ", goal: " + str(cur_edge.state2.to_string()))
                            obs = self.env.gen_obs()

                        else:
                            print("sub task failed :(")
                            finished = True
                            total_successes.append(0)
                            break
        
        print("calculated pareto cost: " + str(path["cost"]))
        print("average cost: " + str(np.average(total_cost)))
        print("calculated pareto probability: " + str(path["probability"]))
        print("success rate: " + str(np.sum(total_successes)/len(total_successes)))
    
    def create_product_graph(self, LTL_string):
        automata = LTL_to_automata(LTL_string)
        bdict = automata.get_dict()

        #Create product automata
        stateset = []
        final_stateset = []
        start_state_g = None
        edgeset = []
        edgeset_string = []

        # - Create Product state set 
        for stateHLM in self.states:
            for s in range(0, automata.num_states()):
                name = stateHLM.name + "b" + str(s)
                sp = State(name, stateHLM.low_level_state)
                stateset.append(sp)

                if stateHLM == self.start_state and str(s) in str(automata.get_init_state_number()):
                    start_state_g = copy.deepcopy(sp)

                for t in automata.out(s):
                    print("    acc sets =", t.acc)
                    if(len(str(t.acc)) > 2):
                        final_stateset.append(sp)

        for state in stateset:
            print(state.to_string())

        #Create list of variables
        variables = []
        for ap in automata.ap():
            variables.append(str(ap))
        print(str(variables))

        index = 0
        # - Create Product edge set

        def get_state_by_name_from_array(states, name):
            vertex = None
            for cur_state in states:
                if(cur_state.name == name):
                    return cur_state
                      
            return vertex

        for edgeHLM in self.edges:
            for s in range(0, automata.num_states()):
                for edgeAut in automata.out(s):
                    startState = edgeHLM.state1.name + "b" + str(edgeAut.src)
                    endState = edgeHLM.state2.name + "b" + str(edgeAut.dst)
                    
                    expression = solve_edge_bool_expression(bdict, edgeAut, edgeHLM, variables)

                    if(expression):
                        edge = {"start": startState, "end": endState, "label": spot.bdd_format_formula(bdict, edgeAut.cond), "probability": edgeHLM.probability, "cost":edgeHLM.cost} 
                        startStateS = get_state_by_name_from_array(stateset, startState)
                        endStateS = get_state_by_name_from_array(stateset, endState)
                        edgeE = Edge('E' + str(index), edgeHLM.controller, startStateS, endStateS, edgeHLM.probability, edgeHLM.cost, edgeHLM.labels)  
                        edgeset.append(edgeE)
                        print(edgeE.to_string())         
                        edgeset_string.append(edge)
                        print(startStateS.to_string())
                        startStateS.add_outgoing_edge(edgeE)
                        endStateS.add_incoming_edge(edgeE)
                        index += 1

        #TODO prune unreachable states, except start state  

        #filter out all final states that only have ingoing transitions from other final states

        def in_stateset(stateset, name):
            for s in stateset:
                if s.name == name:
                    return True
            
            return False

        final_stateset_copy = copy.deepcopy(final_stateset)
        edgeset_copy = copy.deepcopy(edgeset)
        stateset_copy = copy.deepcopy(stateset)
        for final_state in final_stateset:
            #print("checking state :" + str(final_state.name))
            remove = 0
            for incoming_edge in final_state.incoming_edges:
                #print("incoming state: " + str(incoming_edge.state1.name))
                if in_stateset(final_stateset, incoming_edge.state1.name) or not in_stateset(stateset, incoming_edge.state1.name):
                    remove += 1

            if remove == len(final_state.incoming_edges):
                print("remove state: " + str(final_state.name))
                edgeset_copy = [e for e in edgeset_copy if e.state2.name != final_state.name]
                edgeset_copy = [e for e in edgeset_copy if e.state1.name != final_state.name]
                stateset_copy = [s for s in stateset_copy if s.name != final_state.name] 
                final_stateset_copy = [fs for fs in final_stateset_copy if fs.name != final_state.name]

        edgeset = edgeset_copy
        stateset = stateset_copy
        final_stateset = final_stateset_copy

        #filter out states without any incoming transitions, except starting state and their outgoing edges
        
        # contains_unreachable_states = True

        # while contains_unreachable_states:
        #     contains_unreachable_states = False
        #     for state in stateset:
        #         if len(state.incoming_edges) == 0 and state.name != start_state_g.name:
        #             #print("removing: " + str(state.name))
        #             contains_unreachable_states = True

        #             edgeset = [e for e in edgeset if e.state1.name != state.name]
        #             stateset = [s for s in stateset if s.name != state.name] 
        #             final_stateset = [fs for fs in final_stateset if fs.name != state.name]

        for state in stateset:
            print(str(state.name))

        # - Connect Correct states and edges
        graph = Graph(stateset, start_state_g, final_stateset, edgeset)
        return graph

    def print_edges(self):
        for edge in self.edges:
            print(edge.to_string())

    def print_states(self):
        for state in self.states:
            print(state.to_string())

    def show_HLM_graph(self):
        '''
        Generate a graph displaying the model
        '''
        
        final_states = []
        final_states.append(get_state(self, self.goal_state))
        g = Graph(self.states, get_state(self, self.start_state), final_states, self.edges)
        
        g.show_graph('high level model')
