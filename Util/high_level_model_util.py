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

def find_controller(HLM, start_state, end_state):
    for controller in HLM.controllers:
        if controller.start_state == start_state and controller.goal_state == end_state:
            return controller

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