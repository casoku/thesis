def find_edge_states(HLM, task):
    start_state = None
    end_state = None
    for state in HLM.states:
        if state.low_level_state == task.start_state:
            start_state = state

        if state.low_level_state == task.goal_state:
            end_state = state

    return start_state, end_state 

def find_controller(HLM, start_state, end_state):
    for controller in HLM.controllers:
        if controller.start_state == start_state and controller.goal_state == end_state:
            return controller