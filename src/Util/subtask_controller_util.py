
import os
import numpy as np


def create_controller_save_files(save_dir=None, HLM_save=False, model=None):
        assert save_dir is not None
        assert model is not None

        save_path = None
        if HLM_save:
            save_path = save_dir
        else:
            save_path = os.path.join('Subcontrollers', save_dir)
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        model_file = os.path.join(save_path, 'model')
        model.save(model_file)
        controller_file = os.path.join(save_path, 'controller_data.p')

        return controller_file

def load_controller_files(load_dir=None, HLM_load=False):
    assert load_dir is not None

    if HLM_load:
        load_path = load_dir
    else:
        load_path = os.path.join('Subcontrollers', load_dir)


    controller_file = os.path.join(load_path, 'controller_data.p')
    model_file = os.path.join(load_path, 'model')

    return controller_file, model_file

def calculate_step_data(steps_array=None):
    assert steps_array is not None

    avg_num_steps = 0
    std_num_steps = 0
    if len(steps_array) > 0:
        avg_num_steps = round(np.mean(steps_array))
        std_num_steps = round(np.std(steps_array))

    return avg_num_steps, std_num_steps
