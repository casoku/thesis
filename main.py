from copy import deepcopy
from Util.Edge import Edge
from Util.Graph import Graph
from Util.State import State
from Environment_simple import Environment_simple
from Util.Objective import Objective
from Util.automata_util import * 
from Environment import Environment
from high_level_model import HLM
import spot

def get_state_by_name(states, name):
    vertex = None
    for cur_state in states:
        if(cur_state.name == name):
            vertex = cur_state
            break
    
    return vertex

goal_state = [13, 13] # The final goal state to reach in the complex environment
goal_1 = {'state': [13, 13], 'color': 'green'}
goal_2 = {'state': [13, 1], 'color': 'purple'}
goal_states = []
goal_states.append(goal_1)
goal_states.append(goal_2)
start_state = [1,1]
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

#env = Environment_simple(**env_settings)

'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
#Objective(start_state, goal_state, observation_top, observation_width, observation_height)
# Room Top-left objectives
objective1 = Objective([1,1], [7,3], [0,0], 8, 8)
objectives.append(objective1)
objective1r = Objective([7,3], [1,1], [0,0], 8, 8)
objectives.append(objective1r)

objective2 = Objective([1,1], [3,7], [0,0], 8, 8)
objectives.append(objective2)
objective2r = Objective([3,7], [1,1], [0,0], 8, 8)
objectives.append(objective2r)

objective7 = Objective([3,7],[7,3], [0,0], 8, 8)
objectives.append(objective7)
objective7r = Objective([7,3], [3,7], [0,0], 8, 8)
objectives.append(objective7r)

#Room Top-right objectives
objective3 = Objective([7,3], [10,7], [7,0], 8, 8)
objectives.append(objective3)
objective3r = Objective([10,7], [7,3], [7,0], 8, 8)
objectives.append(objective3r)
objectiveP1 = Objective([7,3], [13,1], [7,0], 8, 8, ['p'])
objectives.append(objectiveP1)
objectiveP1r = Objective([13,1], [7,3], [7,0], 8, 8)
objectives.append(objectiveP1r)
objectiveP2 = Objective([10,7], [13,1], [7,0], 8, 8, ['p'])
objectives.append(objectiveP2)
objectiveP2r = Objective([13,1], [10,7], [7,0], 8, 8)
objectives.append(objectiveP2r)

#Room Bottom-left objectives
objective4 = Objective([3,7], [7,10], [0,7], 8, 8)
objectives.append(objective4)
objective4r = Objective([7,10], [3,7], [0,7], 8, 8)
objectives.append(objective4r)

#Room Bottom-right objectives
objective5 = Objective([7,10], [13,13], [7,7], 8, 8, ['g'])
objectives.append(objective5)
objective5r = Objective([13,13], [7,10], [7,7], 8, 8)
objectives.append(objective5r)

objective6 = Objective([10,7], [13,13], [7,7], 8, 8, ['g'])
objectives.append(objective6)
objective6r = Objective([13,13], [10,7], [7,7], 8, 8)
objectives.append(objective6r)

objective8 = Objective([10, 7], [7, 10],[7,7], 8, 8)
objectives.append(objective8)
objective8r = Objective([7, 10], [10, 7], [7,7], 8, 8)
objectives.append(objective8r)

# high_level_model = HLM(objectives, start_state, goal_state, env)
# high_level_model.train_subcontrollers()
# high_level_model.save('full_HLM')

high_level_model = None
high_level_model = HLM(load_dir='full_HLM')

#high_level_model.print_controllers_performance()
#high_level_model.martins_algorithm()

# for state in high_level_model.states:
#     for label in state.permanent_labels:
#         print(label.to_string())

# paths = high_level_model.find_optimal_paths()
# print(paths)
#high_level_model.demonstrate_capabilities()
#high_level_model.demonstrate_HLC(path=paths[0])
#high_level_model.generate_graph()

high_level_model.print_edges()
high_level_model.print_states()

automata = LTL_to_automata('F(p & F g)')
bdict = automata.get_dict()

custom_print(automata)

#show_automata(automata)


#Create product automata
stateset = []
final_stateset = []
start_state_g = None
edgeset = []
edgeset2 = []

acceptance = str(automata.get_acceptance())
# - Create Product state set 
for stateHLM in high_level_model.states:
    for s in range(0, automata.num_states()):
        name = stateHLM.name + "b" + str(s)
        sp = State(name, stateHLM.low_level_state)
        stateset.append(sp)

        if stateHLM == start_state and str(s) in str(automata.get_init_state_number()):
            print("guuyyyy")
            start_state_g = deepcopy(sp)

        if(str(s) in acceptance):
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
for edgeHLM in high_level_model.edges:
    for s in range(0, automata.num_states()):
        for edgeAut in automata.out(s):
            startState = edgeHLM.state1.name + "b" + str(edgeAut.src)
            endState = edgeHLM.state2.name + "b" + str(edgeAut.dst)
            
            expression = solve_edge_bool_expression(bdict, edgeAut, edgeHLM, variables)

            if(expression):
                edge = {"start": startState, "end": endState, "label": spot.bdd_format_formula(bdict, edgeAut.cond), "probability": edgeHLM.probability, "cost":edgeHLM.cost} 
                edgeE = Edge('E' + str(index), edgeHLM.controller, get_state_by_name(stateset, startState), get_state_by_name(stateset, endState), edgeHLM.cost, edgeHLM.probability, edgeHLM.labels)  
                edgeset2.append(edgeE)
                print(edgeE.to_string())         
                edgeset.append(edge)
                index += 1

for edge in edgeset:
    print(edge)

print(len(edgeset))
print(final_stateset)
print(start_state_g)
#TODO prune unreachable edges, except start state

# - Connect Correct states and edges
graph = Graph(stateset, start_state_g, final_stateset, edgeset2)

graph.show_graph()
# - Highlight start state and goal states
