from Environment_simple import Environment_simple
from Environment_9_rooms import Environment_9_rooms 

def create_simple_env():
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
    return env

def create_9_rooms_env():
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
    return env
