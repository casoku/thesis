from Environment_simple import Environment_simple
from Util.Objective import Objective
from Util.automata_util import * 
from high_level_model import HLM
from Util.PAC import calculate_PAC


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

# high_level_model = HLM(objectives, start_state, goal_state, env)
# high_level_model.train_subcontrollers(epochs = 2000)
# high_level_model.save('simple_env_small_subtasks')
# del high_level_model

high_level_model = None
high_level_model = HLM(load_dir='simple_env_small_subtasks')

#LTL = 'F p | F g'
#LTL = 'F (g & F p)'
#LTL = 'F g'
LTL = 'F g & G ! r3'
#LTL = 'F (g & F( p  & F (g & F start)))'

automata = LTL_to_automata(LTL)
bdict = automata.get_dict()

custom_print(automata)

show_automata(automata)
high_level_model.show_HLM_graph()

graph = high_level_model.create_product_graph(LTL)
graph.martins_algorithm()
paths = graph.find_optimal_paths_2()
print(paths)

graph.show_graph('product graph')
dict = high_level_model.demonstrate_HLC(path=paths[0], n_episodes=1, render = False)
PAC_upper_probability = dict["probability"] + 0.05 * dict["probability"]
PAC_lower_probability = dict["probability"] - 0.05 * dict["probability"]
PAC_upper_cost = dict["cost"] + 0.05 * dict["cost"]
PAC_lower_cost = dict["cost"] - 0.05 * dict["cost"]
print("--------------------------------------")
print("PAC upper Probability: " + str(PAC_upper_probability))
print("PAC lower Probability: " + str(PAC_lower_probability))
print("PAC upper Cost: " + str(PAC_upper_cost))
print("PAC lower Cost: " + str(PAC_lower_cost))