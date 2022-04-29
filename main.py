from Util.Objective import Objective
from Environment import Environment
from high_level_model import HLM

goal_state = [11, 11] # The final goal state to reach in the complex environment
start_state = [1,1]
'''
Create environment in which the high-level-controller will be tested
'''
env_settings = {
    'agent_start_states' : start_state,
    'goal_states': goal_state,
    'slip_p' : 0,
    'width' : 13,
    'height' : 13
}
env = Environment(**env_settings)

'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
#Objective(start_state, goal_state, observation_top, observation_width, observation_height)
objective1 = Objective([1,1], [6,3], [0,0], 7, 7)
objectives.append(objective1)
objective1r = Objective([6,3], [1,1], [0,0], 7, 7)
objectives.append(objective1r)

objective2 = Objective([1,1], [3,6], [0,0], 7, 7)
objectives.append(objective2)
objective2r = Objective([3,6], [1,1], [0,0], 7, 7)
objectives.append(objective2r)

objective3 = Objective([6,3], [9,6], [6,0], 7, 7)
objectives.append(objective3)
objective3r = Objective([9,6], [6,3], [6,0], 7, 7)
objectives.append(objective3r)

objective4 = Objective([3,6], [6,9], [0,6], 7, 7)
objectives.append(objective4)
objective4r = Objective([6,9], [3,6], [0,6], 7, 7)
objectives.append(objective4r)

objective5 = Objective([6,9], [11,11], [6,6], 7, 7)
objectives.append(objective5)
objective5r = Objective([11,11], [6,9], [6,6], 7, 7)
objectives.append(objective5r)

objective6 = Objective([9,6], [11,11], [6,6], 7, 7)
objectives.append(objective6)
objective6r = Objective([11,11], [9,6], [6,6], 7, 7)
objectives.append(objective6r)

objective7 = Objective([3,6],[6,3], [0,0], 7, 7)
objectives.append(objective7)
objective7r = Objective([6,3], [3,6], [0,0], 7, 7)
objectives.append(objective7r)

objective8 = Objective([6, 9], [9, 6],[6,6], 7, 7)
objectives.append(objective8)
objective8r = Objective([9, 6], [6, 9], [6,6], 7, 7)
objectives.append(objective8r)

high_level_model = HLM(objectives, start_state, goal_state, env)
high_level_model.train_subcontrollers()
high_level_model.save('full_HLM')

high_level_model = None
high_level_model = HLM(load_dir='full_HLM')

high_level_model.demonstrate_capabilities()
#high_level_model.generate_graph()
high_level_model.print_controllers_performance()

