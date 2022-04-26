from Environment_deterministic import Deterministic_Environment
from Util.Objective import Objective
from Environment import Environment
from high_level_model import HLM

goal_state = [11, 11] # The final goal state to reach in the complex environment
start_state = [1,1]
'''
Create environment in which the high-level-controller will be tested
'''
env_settings = {
    'agent_start_states' : [1,1],
    'goal_states': [2, 24],
    'slip_p' : 0,
    'width' : 29,
    'height' : 29,
    'obstacles_per_room': 0
}
env = Deterministic_Environment(**env_settings)

'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
#Objective(start_state, goal_state, observation_top, observation_width, observation_height)
objective1 = Objective([1,1], [7,4], [0,0], 7, 7)
objectives.append(objective1)
objective1r = Objective([7,4], [1,1], [0,0], 7, 7)
objectives.append(objective1r)

# objective2 = Objective([1,1], [3,7], [0,0], 8, 8)
# objectives.append(objective2)
# objective2r = Objective([3,7], [1,1], [0,0], 8, 8)
# objectives.append(objective2r)

# objective3 = Objective([7,4], [3,7], [0,0], 8, 8)
# objectives.append(objective3)
# objective3r = Objective([3,7], [7,4], [0,0], 8, 8)
# objectives.append(objective3r)

high_level_model = HLM(objectives, start_state, goal_state, env)
high_level_model.train_subcontrollers()
high_level_model.save('deterministic_HLM')

high_level_model = None
high_level_model = HLM(load_dir='deterministic_HLM')

high_level_model.demonstrate_capabilities()
#high_level_model.generate_graph()

