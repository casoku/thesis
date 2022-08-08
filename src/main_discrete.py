from Environment_simple import Environment_simple
from Util.Objective import Objective
from Util.automata_util import * 
from high_level_model import HLM
from Environment_discrete import Environment_discrete_rooms


def get_state_by_name(states, name):
    vertex = None
    for cur_state in states:
        if(cur_state.name == name):
            vertex = cur_state
            break
    
    return vertex

goal_1 = {'state': [1, 6], 'color': 'green'}
goal_2 = {'state': [13, 1], 'color': 'yellow'}
goal_3 = {'state': [13, 8], 'color': 'purple'}
goal_states = []
goal_states.append(goal_1)
goal_states.append(goal_2)
goal_states.append(goal_3)
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
env = Environment_discrete_rooms(**env_settings)

'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
#Objective(start_state, goal_state, observation_top, observation_width, observation_height)
# Room Top-left objectives
objective1 = Objective([1,1], [7,3], [0,0], 8, 8, ['r2'])
objectives.append(objective1)
objective1r = Objective([7,3], [1,1], [0,0], 8, 8, ['s'])
objectives.append(objective1r)

objective2 = Objective([1,1], [3,7], [0,0], 8, 8, ['r3'])
objectives.append(objective2)
objective2r = Objective([3,7], [1,1], [0,0], 8, 8, ['s'])
objectives.append(objective2r)

objective3 = Objective([1,1], [1,6], [0,0], 8, 8, ['g'])
objectives.append(objective3)
objective3r = Objective([1,6], [1,1], [0,0], 8, 8, ['s'])
objectives.append(objective3r)

objective4 = Objective([7,3], [3,7], [0,0], 8, 8, ['r3'])
objectives.append(objective4)
objective4r = Objective([3,7], [7,3], [0,0], 8, 8, ['r2'])
objectives.append(objective4r)

objective5 = Objective([7,3], [1,6], [0,0], 8, 8, ['g'])
objectives.append(objective5)
objective5r = Objective([1,6], [7,3], [0,0], 8, 8, ['r2'])
objectives.append(objective5r)

objective6 = Objective([3,7], [1,6], [0,0], 8, 8, ['g'])
objectives.append(objective6)
objective6r = Objective([1,6], [3,7], [0,0], 8, 8, ['r3'])
objectives.append(objective6r)

#Room Top-right objectives
objective7 = Objective([7,3], [13,1], [7,0], 8, 8, ['y'])
objectives.append(objective7)
objective7r = Objective([13,1], [7,3], [7,0], 8, 8, ['r1'])
objectives.append(objective7r)

objective8 = Objective([7,3], [10,7], [7,0], 8, 8, ['r4'])
objectives.append(objective8)
objective8r = Objective([10,7], [7,3], [7,0], 8, 8, ['r1'])
objectives.append(objective8r)

objective9 = Objective([10,7], [13,1], [7,0], 8, 8, ['y'])
objectives.append(objective9)
objective9r = Objective([13,1], [10,7], [7,0], 8, 8, ['r4'])
objectives.append(objective9r)

#Room Bottom-left objectives
objective10 = Objective([3,7], [7,10], [0,7], 8, 8, ['r4'])
objectives.append(objective10)
objective10r = Objective([7,10], [3,7], [0,7], 8, 8, ['r1'])
objectives.append(objective10r)

#Room Bottom-right objectives
objective11 = Objective([10,7], [13,8], [7,7], 8, 8, ['p'])
objectives.append(objective11)
objective11r = Objective([13,8], [10,7], [7,7], 8, 8, ['r2'])
objectives.append(objective11r)

objective12 = Objective([10,7], [7,10], [7,7], 8, 8, ['r3'])
objectives.append(objective12)
objective12r = Objective([7,10], [10,7], [7,7], 8, 8, ['r2'])
objectives.append(objective12r)

objective13 = Objective([7,10], [13,8], [7,7], 8, 8, ['p'])
objectives.append(objective13)
objective13r = Objective([13,8], [7,10], [7,7], 8, 8, ['r3'])
objectives.append(objective13r)


high_level_model = HLM(objectives, start_state, goal_state, env)
high_level_model.train_subcontrollers()
high_level_model.save('deterministic_HLM_2')

high_level_model = None
high_level_model = HLM(load_dir='deterministic_HLM_2')

LTL = "F p & F g & F y"
automata = LTL_to_automata(LTL)
bdict = automata.get_dict()

custom_print(automata)

show_automata(automata)
high_level_model.show_HLM_graph()

graph = high_level_model.create_product_graph(LTL)
graph.martins_algorithm()
print("----")
paths = graph.find_optimal_paths_2()
print(paths)

graph.show_graph('product graph')
high_level_model.demonstrate_HLC(path=paths[0], n_episodes=5, render = True)
