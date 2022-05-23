import os

def find_edge_states(HLM, task):
    start_state = None
    end_state = None
    for state in HLM.states:
        if state.low_level_state == task.start_state:
            start_state = state

        if state.low_level_state == task.goal_state:
            end_state = state

    return start_state, end_state 

def find_edge_by_states(HLM, start_state, end_state):
    for edge in HLM.edges:
        if edge.state1 == start_state and edge.state2 == end_state:
            return edge
    
    return None

def find_controller(HLM, start_state, end_state):
    for controller in HLM.controllers:
        if controller.start_state == start_state and controller.goal_state == end_state:
            return controller

def get_state_by_name(HLM, name):
    for state in HLM.states:
        if(state.name == name):
            return state

    return None

def get_state(HLM, state):
    vertex = None
    for cur_state in HLM.states:
        if(cur_state == state):
            vertex = cur_state
            break
    
    return vertex


def create_HLM_save_files(save_dir):
    #Create path and folder to save HLM in
    save_path = os.path.join('Models', save_dir)
    if not os.path.isdir(save_path):
        os.mkdir(save_path)

    #Create subfolder to save subcontrollers of this HLM in
    subcontrollers_path = os.path.join('Models', save_dir, 'Subcontrollers')
    if not os.path.isdir(subcontrollers_path):
        os.mkdir(subcontrollers_path)

    # Create the save file for the models
    model_file = os.path.join(save_path, 'model_data.p')

    return model_file, subcontrollers_path