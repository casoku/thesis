from Environment_simple import Environment_simple
from Util.Objective import Objective
from Util.automata_util import * 
from Util.pareto_graph import pareto_graph
from high_level_model import HLM
from Util.PAC import calculate_PAC

import numpy as np
from math import sqrt, pow, exp

def get_state_by_name(states, name):
    vertex = None
    for cur_state in states:
        if(cur_state.name == name):
            vertex = cur_state
            break
    
    return vertex

goal_1 = {'state': [13, 13], 'color': 'green'}
goal_2 = {'state': [13, 1], 'color': 'purple'}
goal_states = []
goal_states.append(goal_1)
goal_states.append(goal_2)
start_state = [1,1]
goal_state = [13,13]
'''
Create environment in which the high-level-controller will be tested
'''
env_settings = {
    'agent_start_states' : start_state,
    'goal_states': goal_states,
    'slip_p' : 0,
    'width' : 15,
    'height' : 15
}

env = Environment_simple(**env_settings)

'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
#Objective(start_state, goal_state, observation_top, observation_width, observation_height)
# Room Top-left objectives
objective1 = Objective([1,1], [7,3], [0,0], 8, 8, ['d1'], ['r1'])
objectives.append(objective1)
objective1r = Objective([7,3], [1,1], [0,0], 8, 8, ['start'], ['r1'])
objectives.append(objective1r)

objective2 = Objective([1,1], [3,7], [0,0], 8, 8, ['d2'], ['r1'])
objectives.append(objective2)
objective2r = Objective([3,7], [1,1], [0,0], 8, 8, ['start'], ['r1'])
objectives.append(objective2r)

objective7 = Objective([3,7],[7,3], [0,0], 8, 8, ['d1'], ['r1'])
objectives.append(objective7)
objective7r = Objective([7,3], [3,7], [0,0], 8, 8, ['d2'], ['r1'])
objectives.append(objective7r)

#Room Top-right objectives
objective3 = Objective([7,3], [10,7], [7,0], 8, 8, ['d3'], ['r2'])
objectives.append(objective3)
objective3r = Objective([10,7], [7,3], [7,0], 8, 8, ['d1'], ['r2'])
objectives.append(objective3r)
objectiveP1 = Objective([7,3], [13,1], [7,0], 8, 8, ['p'], ['r2'])
objectives.append(objectiveP1)
objectiveP1r = Objective([13,1], [7,3], [7,0], 8, 8, ['d1'], ['r2'])
objectives.append(objectiveP1r)
objectiveP2 = Objective([10,7], [13,1], [7,0], 8, 8, ['p'], ['r2'])
objectives.append(objectiveP2)
objectiveP2r = Objective([13,1], [10,7], [7,0], 8, 8, ['d3'], ['r2'])
objectives.append(objectiveP2r)

#Room Bottom-left objectives
objective4 = Objective([3,7], [7,10], [0,7], 8, 8, ['d4'], ['r3'])
objectives.append(objective4)
objective4r = Objective([7,10], [3,7], [0,7], 8, 8, ['d2'], ['r3'])
objectives.append(objective4r)

#Room Bottom-right objectives
objective5 = Objective([7,10], [13,13], [7,7], 8, 8, ['g'], ['r4'])
objectives.append(objective5)
objective5r = Objective([13,13], [7,10], [7,7], 8, 8, ['d4'], ['r4'])
objectives.append(objective5r)

objective6 = Objective([10,7], [13,13], [7,7], 8, 8, ['g'], ['r4'])
objectives.append(objective6)
objective6r = Objective([13,13], [10,7], [7,7], 8, 8, ['d3'], ['r4'])
objectives.append(objective6r)

objective8 = Objective([10, 7], [7, 10],[7,7], 8, 8, ['d4'], ['r4'])
objectives.append(objective8)
objective8r = Objective([7, 10], [10, 7], [7,7], 8, 8, ['d3'], ['r4'])
objectives.append(objective8r)

objectivesB = []
# BIG SUBTASKS
objectiveB1 = Objective([1,1], [13,1], [0,0], 15, 15, ['p'], ['r1, r2'])
objectivesB.append(objectiveB1)
objectiveB1r = Objective([13,1], [1,1], [0,0], 15, 15, ['start'], ['r1, r2'])
objectivesB.append(objectiveB1r)

objectiveB2 = Objective([1,1], [13,13], [0,0], 15, 15, ['g'], ['r1, r2, r3, r4'])
objectivesB.append(objectiveB2)
objectiveB2r = Objective([13,13], [1,1], [0,0], 15, 15, ['start'], ['r1, r2', 'r3', 'r4'])
objectivesB.append(objectiveB2r)

objectiveB3 = Objective([13,1], [13,13], [0,0], 15, 15, ['g'], ['r2, r4'])
objectivesB.append(objectiveB3)
objectiveB3r = Objective([13,13], [13,1], [0,0], 15, 15, ['p'], ['r2, r4'])
objectivesB.append(objectiveB3r)

# high_level_model = HLM(objectives, start_state, goal_state, env)
# high_level_model.train_subcontrollers(epochs = 50000, save_dir='simple_env_small_subtasks')
# high_level_model.save('simple_env_small_subtasks')
# del high_level_model

high_level_model = None
high_level_model = HLM(load_dir='simple_env_small_subtasks')

LTL1 = 'F p | F g'
LTL2 = 'F (g & F p)'
LTL3 = 'F g'
LTL4 = 'F g & G ! r3'
LTL5 = 'F (g & F( p  & F (g & F start)))'
LTL6 = '! r2 U g & F p'

specs = [LTL1, LTL2, LTL3, LTL4, LTL5]
cost_lower_bound = [16, 42, 24, 84, 26, 63, 93]
cost_upper_bound = [x * 3 for x in cost_lower_bound]
error_margin = [x * 0.05 for x in cost_upper_bound]
index = 0
for LTL in specs:
    print('---------------------- Task {}----------------------'.format(LTL))
    automata = LTL_to_automata(LTL)
    bdict = automata.get_dict()

    #custom_print(automata)

    #show_automata(automata)
    #high_level_model.show_HLM_graph()

    graph = high_level_model.create_product_graph(LTL)
    graph.martins_algorithm()
    paths_1, filtered_paths_1 = graph.find_optimal_paths()
    paths = graph.find_optimal_paths_2()
    print("------------------------------------")
    print("num of paths: " + str(len(paths_1)))
    print("num of filtere paths: " + str(len(filtered_paths_1)))
    print("num of paths method 2: " + str(len(paths)))
    print("------------------------------------")

    #pareto_graph(paths)

    #graph.show_graph('product graph')
    for path in paths:
        dict = high_level_model.demonstrate_HLC(path=path, n_episodes=600, render = False)

        # mean_succ = []
        # for i in range(20):
        #     dict = high_level_model.demonstrate_HLC(path=paths[0], n_episodes=600, render = False, save=False)
        #     mean_succ.append(dict['probability'])

        # mean_mean = np.mean(mean_succ)
        # var = [] 

        # for m in mean_succ:
        #     var.append(pow((m - mean_mean), 2))

        # std = np.sum(var)/(20)
        
        # print(std)
        PAC_upper_probability = dict["probability"] + 0.05 
        PAC_lower_probability = dict["probability"] - 0.05
        # PAC_upper_cost = dict["cost"] + 0.05 * dict["cost"]
        # PAC_lower_cost = dict["cost"] - 0.05 * dict["cost"]
        print("--------------------------------------")
        print("PAC lower Probability: " + str(PAC_lower_probability))
        print("PAC upper Probability: " + str(PAC_upper_probability))
        print("--------------------------------------")
        estimated_cost = dict["cost"]
        print("PAC estiamted cost: " + str(estimated_cost))
        print("PAC cost lower bound: " + str(dict["cost"] - error_margin[index]))
        print("PAC cost upper bound: " + str(dict["cost"] + error_margin[index]))
        num_of_samples = np.sum(dict["total_successes"])
        print("num of samples: " + str(num_of_samples))
        print("error margin: " + str(error_margin[index]))
        PAC = 2 * exp((-((2*num_of_samples*pow(error_margin[index], 2))/(pow((cost_upper_bound[index] - cost_lower_bound[index]), 2)))))
        print ("delta : " + str(round(PAC, 3)))
        print ("probaiblity True mean cost is within error margin: " + str(round((1 - PAC), 3)))
        # print("PAC upper Cost: " + str(PAC_upper_cost))
        # print("PAC lower Cost: " + str(PAC_lower_cost))
        index += 1