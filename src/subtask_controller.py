import copy
import pickle
from stable_baselines3 import HerReplayBuffer, DDPG, DQN, SAC, TD3, PPO, A2C

from Util.subtask_controller_util import *


class SubtaskController(object):
    """
    Class representing a goal-oriented sub-task within the environment
    """
    def __init__(self, controller_id=None, start_state=None, goal_state=None, observation_width=7, observation_height=7, observation_top=[0, 0], env=None, max_training_steps=1e6, load_dir=None, HLM_load=False, verbose=False):
        self.id = controller_id
        self.start_state = start_state
        self.goal_state = goal_state
        self.observation_width = observation_width
        self.observation_height = observation_height
        self.observation_top = observation_top
        self.env = copy.deepcopy(env)
        self.max_training_steps = max_training_steps
        self.training_steps = 0
        self.verbose = verbose

        self.data = {
            'total_training_steps' : 0,
            'performance_estimates' : {},
            'required_success_prob' : 0,
        }

        if load_dir is None:
            assert controller_id is not None
            assert start_state is not None
            assert goal_state is not None
            assert env is not None
            self._set_training_env(env)
            self._init_learning_alg(verbose=self.verbose)
        else:
            self.load(load_dir, HLM_load=HLM_load)
    
    def learn(self, total_timesteps=5e4):
        """
        Train the sub-system for a specified number of timesteps.
        """
        self.model.learn(total_timesteps=total_timesteps)
        self.training_steps = total_timesteps
        #self.data['total_training_steps'] = self.data['total_training_steps'] + total_timesteps

    def save(self, save_dir=None, HLM_save=False):
        """
        Save the controller object.
        """
        controller_file = create_controller_save_files(save_dir, HLM_save, self.model)
        
        controller_data = {
            'controller_id' : self.id,
            'start_state' : self.start_state,
            'goal_state' : self.goal_state,
            'observation_width': self.observation_width,
            'observation_height': self.observation_height,
            'observation_top': self.observation_top,
            'env' : self.env,
            'verbose' : self.verbose,
            'max_training_steps' : self.max_training_steps,
            'training_steps': self.training_steps,
            'data' : self.data,
        }

        with open(controller_file, 'wb') as pickleFile:
            pickle.dump(controller_data, pickleFile)

    def load(self, load_dir=None, HLM_load = False):
        """
        Load a controller object
        """

        controller_file, model_file = load_controller_files(load_dir, HLM_load)

        with open(controller_file, 'rb') as pickleFile:
            controller_data = pickle.load(pickleFile)

        self.id = controller_data['controller_id']
        self.start_state = controller_data['start_state']
        self.goal_state = controller_data['goal_state']
        self.observation_width = controller_data['observation_width']
        self.observation_height = controller_data['observation_height']
        self.observation_top = controller_data['observation_top']
        self.env = controller_data['env']
        self.max_training_steps = controller_data['max_training_steps']
        self.training_steps = controller_data['training_steps']
        self.verbose = controller_data['verbose']
        self.data = controller_data['data']
        
        print(self.data)

        self._set_training_env(self.env)
        self.model = PPO.load(model_file, env=self.training_env)
        
    def predict(self, obs, deterministic=True):
        """
        Get the sub-system's action, given the current environment observation (state)
        """
        action, _states = self.model.predict(obs, deterministic=deterministic)
        return action, _states

    def _set_training_env(self, env=None):
        """
        Set the training environment to a newly genereted instance of the environment
        Set the observation size to the subgrid required for this subtask
        Set the start and goal state 
        """
        assert env is not None

        self.training_env = copy.deepcopy(env)
        self.training_env.reset()
        self.training_env.set_observation_size(self.observation_width, self.observation_height, self.observation_top)
        self.training_env.agent_start_states = self.start_state
        self.training_env.sub_task_goal = self.goal_state

    def _init_learning_alg(self, verbose=None):
        self.model = PPO("MlpPolicy", 
                    self.training_env, 
                    verbose=verbose)

        #self.model = A2C("MlpPolicy", self.training_env, verbose=1)
    
    def eval_performance(self, n_episodes=400, n_steps=100, total_steps=0):
        """
        Perform empirical evaluation of the performance of the learned controller.
        """
        success_count = 0
        trials = 0
        num_steps = 0

        steps = []

        for episode_ind in range(n_episodes):
            trials = trials + 1

            obs = self.training_env.reset()
            num_steps = 0
            for step_ind in range(n_steps):
                num_steps = num_steps + 1
                total_steps = total_steps + 1
                action, _states = self.model.predict(obs)
                obs, reward, done, info = self.training_env.step(action)
                if done:
                    if info['task_complete']:
                        #avg_num_steps = (avg_num_steps + num_steps) / 2
                        steps.append(num_steps)
                        success_count = success_count + 1
                    break

            avg_num_steps, std_num_steps = calculate_step_data(steps)
            
        self.data['performance_estimates'] = {
            'training_steps' : self.training_steps,
            'success_count' : success_count,
            'success_rate' : round((success_count / trials), 2),
            'num_trials' : trials,
            'avg_num_steps' : avg_num_steps,
            'std_num_steps' : std_num_steps
        }

    def get_performance(self):
        return self.data

    def get_data(self):
        data = self.data['performance_estimates']
        return data['success_rate'], data ['avg_num_steps'], data['std_num_steps']

    def demonstrate_capabilities(self, n_episodes=8, n_steps=50, render=True):
        """
        Demonstrate the capabilities of the learned controller in the environment used to train it.
        """
        for episode_ind in range(n_episodes):
            obs = self.training_env.reset()
            self.training_env.render(highlight=False)
            for step in range(n_steps):
                #print(obs)
                action, _states = self.model.predict(obs)
                obs, reward, done, info = self.training_env.step(action)
                #print(action)
                if render:
                    self.training_env.render(highlight=False)
                if done:
                    print(info)
                    break

        obs = self.training_env.reset()
        return info['task_complete']
    
