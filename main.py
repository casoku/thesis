from Util.Objective import Objective
from minigrid_env import Maze
from subtask_controller import SubtaskController
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
env = Maze(**env_settings)

'''
Create a list of sub-tasks in the environment that are used to generate a HLM
'''
objectives = []
#Objective(initial_state, final_state, observation_top, observation_width, observation_height)
objective1 = Objective([1,1], [6,3], [0,0], 7, 7)
objectives.append(objective1)
objective2 = Objective([1,1], [3,6], [0,0], 7, 7)
objectives.append(objective2)
objective3 = Objective([6,3], [9,6], [6,0], 7, 7)
objectives.append(objective3)
objective4 = Objective([3,6], [6,9], [0,6], 7, 7)
objectives.append(objective4)
objective5 = Objective([6,9], [11,11], [6,6], 7, 7)
objectives.append(objective5)
objective6 = Objective([9,6], [11,11], [6,6], 7, 7)
objectives.append(objective6)

# high_level_model = HLM(objectives, start_state, goal_state, env_settings)

# high_level_model.train_subcontrollers()
# high_level_model.save('test_HLM')
# high_level_model = None
high_level_model = HLM(load_dir='test_HLM')

# high_level_model.create_states()
# high_level_model.create_edges()
high_level_model.demonstrate_capabilities()
#high_level_model.generate_graph()

