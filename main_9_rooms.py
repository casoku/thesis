from Environment_9_rooms import Environment_9_rooms
from Util.Objective import Objective
from high_level_model import HLM

goal_state = [20, 20] # The final goal state to reach in the complex environment
start_state = [1,1]
'''
Create environment in which the high-level-controller will be tested
'''
env_settings = {
    'agent_start_states' : start_state,
    'goal_states': goal_state,
    'slip_p' : 0,
    'width' : 22,
    'height' : 22
}
env = Environment_9_rooms(**env_settings)

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

objective3 = Objective([3,7],[7,3], [0,0], 8, 8)
objectives.append(objective3)
objective3r = Objective([7,3], [3,7], [0,0], 8, 8)
objectives.append(objective3r)

#Room Top-middle objectives
objective4 = Objective([7,3], [10,7], [7,0], 8, 8)
objectives.append(objective4)
objective4r = Objective([10,7], [7,3], [7,0], 8, 8)
objectives.append(objective3r)

objective5 = Objective([7,3], [14,3], [7,0], 8, 8)
objectives.append(objective5)
objective5r = Objective([14,3], [7,3], [7,0], 8, 8)
objectives.append(objective5r)

objective6 = Objective([10,7], [14,3], [7,0], 8, 8)
objectives.append(objective6)
objective6r = Objective([14,3], [10,7], [7,0], 8, 8)
objectives.append(objective6r)

#Room Top-right objectives
objective7 = Objective([14,3], [17,7], [14,0], 8, 8)
objectives.append(objective7)
objective7r = Objective([17,7], [14,3], [14,0], 8, 8)
objectives.append(objective7r)

#Room Middle-left objectives
objective8 = Objective([3,7], [7,10], [0,7], 8, 8)
objectives.append(objective8)
objective8r = Objective([7,10], [3,7], [0,7], 8, 8)
objectives.append(objective8r)

objective9 = Objective([3,7], [3,14], [0,7], 8, 8)
objectives.append(objective9)
objective9r = Objective([3,14], [3,7], [0,7], 8, 8)
objectives.append(objective9r)

objective10 = Objective([3,14], [7,10], [0,7], 8, 8)
objectives.append(objective10)
objective10r = Objective([7,10], [3,14], [0,7], 8, 8)
objectives.append(objective10r)

#Room Middle-middle objectives
objective11 = Objective([7,10], [10,7], [7,7], 8, 8)
objectives.append(objective11)
objective11r = Objective([10,7], [7,10], [7,7], 8, 8)
objectives.append(objective11r)

objective12 = Objective([7,10], [10,14], [7,7], 8, 8)
objectives.append(objective12)
objective12r = Objective([10,14], [7,10], [7,7], 8, 8)
objectives.append(objective12r)

objective13 = Objective([7,10], [14,10], [7,7], 8, 8)
objectives.append(objective13)
objective13r = Objective([14,10], [7,10], [7,7], 8, 8)
objectives.append(objective13r)

objective14 = Objective([14,10], [10,7], [7,7], 8, 8)
objectives.append(objective14)
objective14r = Objective([10,7], [14,10], [7,7], 8, 8)
objectives.append(objective14r)

objective15 = Objective([14,10], [10,14], [7,7], 8, 8)
objectives.append(objective15)
objective15r = Objective([10,14], [14,10], [7,7], 8, 8)
objectives.append(objective15r)

objective16 = Objective([7,10], [14,10], [7,7], 8, 8)
objectives.append(objective16)
objective16r = Objective([14,10], [7,10], [7,7], 8, 8)
objectives.append(objective16r)

#Room Middle-right objectives
objective17 = Objective([14,10], [17,7], [14,7], 8, 8)
objectives.append(objective17)
objective17r = Objective([17,7], [14,10], [14,7], 8, 8)
objectives.append(objective17r)

objective18 = Objective([14,10], [17,14], [14,7], 8, 8)
objectives.append(objective18)
objective18r = Objective([17,14], [14,10], [14,7], 8, 8)
objectives.append(objective18r)

objective19 = Objective([17,7], [17,14], [14,7], 8, 8)
objectives.append(objective19)
objective19r = Objective([17,14], [17,7], [14,7], 8, 8)
objectives.append(objective19r)

#Room Bottom-left objectives
objective20 = Objective([3,14], [7,17], [0,14], 8, 8)
objectives.append(objective20)
objective20r = Objective([7,17], [3,14], [0,14], 8, 8)
objectives.append(objective20r)

#Room Bottom-middle objectives
objective21 = Objective([7,17], [10,14], [7,14], 8, 8)
objectives.append(objective21)
objective21r = Objective([10,14], [7,17], [7,14], 8, 8)
objectives.append(objective21r)

objective22 = Objective([7,17], [14,17], [7,14], 8, 8)
objectives.append(objective22)
objective22r = Objective([14,17], [7,17], [7,14], 8, 8)
objectives.append(objective22r)

objective23 = Objective([14,17], [10,14], [7,14], 8, 8)
objectives.append(objective23)
objective23r = Objective([10,14], [14,17], [7,14], 8, 8)
objectives.append(objective23r)

#Room Bottom-right objectives
objective24 = Objective([14,17], [20,20], [14,14], 8, 8)
objectives.append(objective24)
objective24r = Objective([20,20], [14,17], [14,14], 8, 8)
objectives.append(objective24r)

objective25 = Objective([14,17], [17,14], [14,14], 8, 8)
objectives.append(objective25)
objective25r = Objective([17,14], [14,17], [14,14], 8, 8)
objectives.append(objective25r)

objective26 = Objective([17,14], [20,20], [14,14], 8, 8)
objectives.append(objective26)
objective26r = Objective([20,20], [17,14], [14,14], 8, 8)
objectives.append(objective26r)

# high_level_model = HLM(objectives, start_state, goal_state, env)
# high_level_model.train_subcontrollers()
# high_level_model.save('9_rooms_HLM')

high_level_model = None
high_level_model = HLM(load_dir='9_rooms_HLM')

#high_level_model.demonstrate_capabilities()
#high_level_model.print_controllers_performance()
high_level_model.martins_algorithm()
high_level_model.print_edges()

for state in high_level_model.states:
    for label in state.permanent_labels:
        print(label.to_string())

paths = high_level_model.find_optimal_paths()
print(paths)
high_level_model.demonstrate_HLC(path=paths[0])
#high_level_model.demonstrate_capabilities()
#high_level_model.generate_graph()

