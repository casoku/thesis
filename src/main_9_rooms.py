from Environment_9_rooms import Environment_9_rooms
from Util.Objective import Objective
from Util.automata_util import * 
from Util.pareto_graph import pareto_graph
from Util.martins_util import order_lexicographically_dict
from high_level_model import HLM
import sys

start_state = [1,1]
goal_1 = {'state': [20, 20], 'color': 'green'}
goal_2 = {'state': [1, 20], 'color': 'purple'}
goal_3 = {'state': [20, 6], 'color': 'yellow'}
goal_4 = {'state': [10, 10], 'color': 'cyan'}
goal_states = []
goal_states.append(goal_1)
goal_states.append(goal_2)
goal_states.append(goal_3)
goal_states.append(goal_4)

'''
Create environment in which the high-level-controller will be tested
'''
env_settings = {
    'agent_start_states' : start_state,
    'goal_states': goal_states,
    'slip_p' : 0,
    'width' : 22,
    'height' : 22
}
env = Environment_9_rooms(**env_settings)

# current is id = 17, objective28r, [20,6], [14,3], next is id = 34, objective16, [10,14], [10,7]
'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
# Objective(start_state, goal_state, observation_top, observation_width, observation_height)
# Room Top-left objectives
objective1 = Objective([1,1], [7,3], [0,0], 8, 8, ['d1', 'R1'], ['R1'])
objectives.append(objective1)
objective1r = Objective([7,3], [1,1], [0,0], 8, 8, ['start', 'R1'], ['R1', 'start'])
objectives.append(objective1r)

objective2 = Objective([1,1], [3,7], [0,0], 8, 8, ['d3', 'R1'], ['R1'])
objectives.append(objective2)
objective2r = Objective([3,7], [1,1], [0,0], 8, 8, ['start', 'R1'], ['R1', 'start'])
objectives.append(objective2r)

objective3 = Objective([3,7],[7,3], [0,0], 8, 8, ['d1', 'R1'], ['R1', 'start'])
objectives.append(objective3)
objective3r = Objective([7,3], [3,7], [0,0], 8, 8, ['d3', 'R1'], ['R1', 'start'])
objectives.append(objective3r)

#Room Top-middle objectives
objective4 = Objective([7,3], [10,7], [7,0], 8, 8, ['d4', 'R2'], ['R2'])
objectives.append(objective4)
objective4r = Objective([10,7], [7,3], [7,0], 8, 8, ['d1', 'R2'], ['R2'])
objectives.append(objective3r)

objective5 = Objective([7,3], [14,3], [7,0], 8, 8, ['d2', 'R2'], ['R2'])
objectives.append(objective5)
objective5r = Objective([14,3], [7,3], [7,0], 8, 8, ['d1', 'R2'], ['R2'])
objectives.append(objective5r)

objective6 = Objective([10,7], [14,3], [7,0], 8, 8, ['d2', 'R2'], ['R2'])
objectives.append(objective6)
objective6r = Objective([14,3], [10,7], [7,0], 8, 8, ['d4', 'R2'], ['R2'])
objectives.append(objective6r)

#Room Top-right objectives
objective7 = Objective([14,3], [17,7], [14,0], 8, 8, ['d5', 'R3'], ['R3', 'y'])
objectives.append(objective7)
objective7r = Objective([17,7], [14,3], [14,0], 8, 8, ['d2', 'R3'], ['R3', 'y'])
objectives.append(objective7r)

objective27 = Objective([17,7], [20,6], [14,0], 8, 8, ['y', 'R3'], ['R3', 'y'])
objectives.append(objective27)

##################################
objective27r = Objective([20,6], [17,7], [14,0], 8, 8, ['d5', 'R3'], ['R3'])
objectives.append(objective27r)
##################################

objective28 = Objective([14,3], [20,6], [14,0], 8, 8, ['y', 'R3'], ['R3', 'y'])
objectives.append(objective28)

###################################
objective28r = Objective([20,6], [14,3], [14,0], 8, 8, ['d2', 'R3'], ['R3'])
objectives.append(objective28r)
###################################

#Room Middle-left objectives
objective8 = Objective([3,7], [7,10], [0,7], 8, 8, ['d6', 'R4'], ['R4'])
objectives.append(objective8)
objective8r = Objective([7,10], [3,7], [0,7], 8, 8, ['d3', 'R4'], ['R4'])
objectives.append(objective8r)

objective9 = Objective([3,7], [3,14], [0,7], 8, 8, ['d8', 'R4'], ['R4'])
objectives.append(objective9)
objective9r = Objective([3,14], [3,7], [0,7], 8, 8, ['d3', 'R4'], ['R4'])
objectives.append(objective9r)

objective10 = Objective([3,14], [7,10], [0,7], 8, 8, ['d6', 'R4'], ['R4'])
objectives.append(objective10)
objective10r = Objective([7,10], [3,14], [0,7], 8, 8, ['d8', 'R4'], ['R4'])
objectives.append(objective10r)

#Room Middle-middle objectives
objective11 = Objective([7,10], [10,7], [7,7], 8, 8, ['d4', 'R5'], ['R5', 'c'])
objectives.append(objective11)
objective11r = Objective([10,7], [7,10], [7,7], 8, 8, ['d6', 'R5'], ['R5', 'c'])
objectives.append(objective11r)

objective12 = Objective([7,10], [10,14], [7,7], 8, 8, ['d9', 'R5'], ['R5', 'c'])
objectives.append(objective12)
objective12r = Objective([10,14], [7,10], [7,7], 8, 8, ['d6', 'R5'], ['R5', 'c'])
objectives.append(objective12r)

objective13 = Objective([7,10], [14,10], [7,7], 8, 8, ['d7', 'R5'], ['R5', 'c'])
objectives.append(objective13)
objective13r = Objective([14,10], [7,10], [7,7], 8, 8, ['d6', 'R5'], ['R5', 'c'])
objectives.append(objective13r)

objective14 = Objective([14,10], [10,7], [7,7], 8, 8, ['d4', 'R5'], ['R5', 'c'])
objectives.append(objective14)
objective14r = Objective([10,7], [14,10], [7,7], 8, 8, ['d7', 'R5'], ['R5', 'c'])
objectives.append(objective14r)

objective15 = Objective([14,10], [10,14], [7,7], 8, 8, ['d9', 'R5'], ['R5', 'c'])
objectives.append(objective15)
objective15r = Objective([10,14], [14,10], [7,7], 8, 8, ['d7', 'R5'], ['R5', 'c'])
objectives.append(objective15r)

# ####################################
objective16 = Objective([10,14], [10,7], [7,7], 8, 8, ['d9', 'R5'], ['R5', 'c'])
objectives.append(objective16)
objective16r = Objective([10,7], [10,14], [7,7], 8, 8, ['d4', 'R5'], ['R5', 'c'])
objectives.append(objective16r)
# ####################################

objective29 = Objective([7,10], [10,10], [7,7], 8, 8, ['c', 'R5'], ['R5', 'c'])
objectives.append(objective29)
objective29r = Objective([10,10], [7,10], [7,7], 8, 8, ['d6', 'R5'], ['R5'])
objectives.append(objective29r)

objective30 = Objective([10,7], [10,10], [7,7], 8, 8, ['c', 'R5'], ['R5', 'c'])
objectives.append(objective30)
objective30r = Objective([10,10], [10,7], [7,7], 8, 8, ['d4', 'R5'], ['R5'])
objectives.append(objective30r)

objective31 = Objective([14,10], [10,10], [7,7], 8, 8, ['c', 'R5'], ['R5', 'c'])
objectives.append(objective31)
objective31r = Objective([10,10], [14,10], [7,7], 8, 8, ['d7', 'R5'], ['R5'])
objectives.append(objective31r)

objective32 = Objective([10,14], [10,10], [7,7], 8, 8, ['c', 'R5'], ['R5', 'c'])
objectives.append(objective32)
objective32r = Objective([10,10], [10,14], [7,7], 8, 8, ['d9', 'R5'], ['R5'])
objectives.append(objective32r)

#Room Middle-right objectives
objective17 = Objective([14,10], [17,7], [14,7], 8, 8, ['d5', 'R6'], ['R6'])
objectives.append(objective17)
objective17r = Objective([17,7], [14,10], [14,7], 8, 8, ['d7', 'R6'], ['R6'])
objectives.append(objective17r)

objective18 = Objective([14,10], [17,14], [14,7], 8, 8, ['d10', 'R6'], ['R6'])
objectives.append(objective18)
objective18r = Objective([17,14], [14,10], [14,7], 8, 8, ['d7', 'R6'], ['R6'])
objectives.append(objective18r)

objective19 = Objective([17,7], [17,14], [14,7], 8, 8, ['d10', 'R6'], ['R6'])
objectives.append(objective19)
objective19r = Objective([17,14], [17,7], [14,7], 8, 8, ['d5', 'R6'], ['R6'])
objectives.append(objective19r)

#Room Bottom-left objectives
objective20 = Objective([3,14], [7,17], [0,14], 8, 8, ['d8', 'R7'], ['R7', 'p'])
objectives.append(objective20)
objective20r = Objective([7,17], [3,14], [0,14], 8, 8, ['d11', 'R7'], ['R7', 'p'])
objectives.append(objective20r)

objective33 = Objective([3,14], [1,20], [0,14], 8, 8, ['p', 'R7'], ['R7', 'p'])
objectives.append(objective33)
objective33r = Objective([1,20], [3,14], [0,14], 8, 8, ['d8', 'R7'], ['R7'])
objectives.append(objective33r)

objective34 = Objective([7,17], [1,20], [0,14], 8, 8, ['p', 'R7'], ['R7', 'p'])
objectives.append(objective34)
objective34r = Objective([1,20], [7,17], [0,14], 8, 8, ['d11', 'R7'], ['R7'])
objectives.append(objective34r)

#Room Bottom-middle objectives
objective21 = Objective([7,17], [10,14], [7,14], 8, 8, ['d9', 'R8'], ['R8'])
objectives.append(objective21)
objective21r = Objective([10,14], [7,17], [7,14], 8, 8, ['d11', 'R8'], ['R8'])
objectives.append(objective21r)

objective22 = Objective([7,17], [14,17], [7,14], 8, 8, ['d12', 'R8'], ['R8'])
objectives.append(objective22)
objective22r = Objective([14,17], [7,17], [7,14], 8, 8, ['d11', 'R8'], ['R8'])
objectives.append(objective22r)

objective23 = Objective([14,17], [10,14], [7,14], 8, 8, ['d9', 'R8'], ['R8'])
objectives.append(objective23)
objective23r = Objective([10,14], [14,17], [7,14], 8, 8, ['d12', 'R8'], ['R8'])
objectives.append(objective23r)

#Room Bottom-right objectives
objective24 = Objective([14,17], [20,20], [14,14], 8, 8, ['g', 'R9'], ['R9', 'g'])
objectives.append(objective24)
objective24r = Objective([20,20], [14,17], [14,14], 8, 8, ['d12', 'R9'], ['R9'])
objectives.append(objective24r)

objective25 = Objective([14,17], [17,14], [14,14], 8, 8, ['d10', 'R9'], ['R9', 'g'])
objectives.append(objective25)
objective25r = Objective([17,14], [14,17], [14,14], 8, 8, ['d12', 'R9'], ['R9', 'g'])
objectives.append(objective25r)

objective26 = Objective([17,14], [20,20], [14,14], 8, 8, ['g', 'R9'], ['R9', 'g'])
objectives.append(objective26)
objective26r = Objective([20,20], [17,14], [14,14], 8, 8, ['d10', 'R9'], ['R9'])
objectives.append(objective26r)

#high_level_model = HLM(objectives, start_state, goal_states, env)
# high_level_model.train_subcontrollers(40000, '9_rooms_HLM')
#high_level_model.save('9_rooms_HLM')

high_level_model = None
high_level_model = HLM(load_dir='9_rooms_HLM')
sys.setrecursionlimit(10000)

#LTL1 = 'F y | F g'
#LTL2 = 'F (p & F g)'
#LTL3 = 'G ! p & F g'
#LTL4 = 'G ! d1 & F p'
#LTL5 = 'F g'
#LTL6 = 'G ! d1 & (F (p & F g))'
#LTL7 = 'G ! d1 & (F y & F c & F (p & F g))'

LTL1 = 'F g | F y'
LTL2 = '! R4 U p & ! R7 U g'
LTL3 = 'F y & F c & F p & F g'

#tasks = [LTL1, LTL2, LTL3]
tasks = [LTL2]
for LTL in tasks:
    print('---------------------- Task {}----------------------'.format(LTL))
    automata = LTL_to_automata(LTL)
    bdict = automata.get_dict()

    # #custom_print(automata)

    #show_automata(automata)
    #high_level_model.show_HLM_graph()
    graph = high_level_model.create_product_graph(LTL)
    graph.martins_algorithm()
    paths_2 = graph.find_optimal_paths_2()
    paths, filterer_paths = graph.find_optimal_paths()
    print("---------------Paths---------------")
    # print(paths)
    # print("------------------------------------")
    # print(filterer_paths)
    # print("------------------------------------")
    print("num of paths: " + str(len(paths)))
    print("num of filtered paths: " + str(len(filterer_paths)))
    print("num of paths method 2: " + str(len(paths_2)))
    print("------------------------------------")
    #paths = graph.find_optimal_paths_2()
    # print("------------------------------------")
    # print("num of paths: " + str(len(paths)))
    # print("------------------------------------")
    # graph.show_graph('product graph')

    paths_2 = order_lexicographically_dict(paths_2)

    # index = 1
    # for path in paths_2:
    #     print('---------------------- Task {}----------------------'.format(index))
    #     print("estimated probability: " + str(path['probability']) + " estimated cost: " + str(path['cost']))
    #     print("number of subtasks: " + str(len(path['edges'])))
    #     high_level_model.demonstrate_HLC(path=path, n_episodes=600, render = False)
    #     index += 1
    #     print()
    dict = high_level_model.demonstrate_HLC(path=paths_2[len(paths_2)-1], n_episodes=8, render = True)
    PAC_upper_probability = dict["probability"] + 0.05 
    PAC_lower_probability = dict["probability"] - 0.05
    # PAC_upper_cost = dict["cost"] + 0.05 * dict["cost"]
    # PAC_lower_cost = dict["cost"] - 0.05 * dict["cost"]
    print("--------------------------------------")
    print("PAC lower Probability: " + str(PAC_lower_probability))
    print("PAC upper Probability: " + str(PAC_upper_probability))

    #high_level_model.demonstrate_HLC(path=paths_2[0], n_episodes=2, render = True)

    #pareto_graph(filterer_paths)
    #pareto_graph(paths_2)
