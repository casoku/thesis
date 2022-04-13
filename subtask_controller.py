import os
import pickle
import gym
from minigrid_env import Maze
from stable_baselines3 import A2C, PPO
from stable_baselines3 import DQN
import numpy as np


class SubtaskController(object):
    """
    Class representing a goal-oriented sub-task within the environment
    """
    def __init__(self, controller_id=None, init_state = None, final_state=None, observation_width=7, observation_height = 7, observation_top = [0, 0],env_settings=None, max_training_steps=1e6, load_dir=None, verbose=False):
        self.id = controller_id
        self.init_state = init_state
        self.final_state = final_state
        self.observation_width = observation_width
        self.observation_height = observation_height
        self.observation_top = observation_top
        self.env_settings = env_settings
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
            assert init_state is not None
            assert final_state is not None
            assert env_settings is not None
            self._set_training_env(env_settings)
            self._init_learning_alg(verbose=self.verbose)
        else:
            self.load(load_dir)
    
    def learn(self, total_timesteps = 5e4):
        """
        Train the sub-system for a specified number of timesteps.

        Inputs
        ------
        total_timesteps : int
            Total number of timesteps to train the sub-system for.
        """
        self.model.learn(total_timesteps=total_timesteps)
        self.training_steps = total_timesteps
        #self.data['total_training_steps'] = self.data['total_training_steps'] + total_timesteps


    def save(self, save_dir):
        """
        Save the controller object.
        """
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        model_file = os.path.join(save_dir, 'model')
        self.model.save(model_file)
        controller_file = os.path.join(save_dir, 'controller_data.p')

        controller_data = {
            'controller_id' : self.id,
            'init_state' : self.init_state,
            'final_state' : self.final_state,
            'observation_width': self.observation_width,
            'observation_height': self.observation_height,
            'observation_top': self.observation_top,
            'env_settings' : self.env_settings,
            'verbose' : self.verbose,
            'max_training_steps' : self.max_training_steps,
            'training_steps': self.training_steps,
            'data' : self.data,
        }

        with open(controller_file, 'wb') as pickleFile:
            pickle.dump(controller_data, pickleFile)

    def load(self, save_dir):
        """
        Load a controller object
        """

        controller_file = os.path.join(save_dir, 'controller_data.p')
        with open(controller_file, 'rb') as pickleFile:
            controller_data = pickle.load(pickleFile)

        self.id = controller_data['controller_id']
        self.init_state = controller_data['init_state']
        self.final_state = controller_data['final_state']
        self.observation_width = controller_data['observation_width']
        self.observation_height = controller_data['observation_height']
        self.observation_top = controller_data['observation_top']
        self.env_settings = controller_data['env_settings']
        self.max_training_steps = controller_data['max_training_steps']
        self.training_steps = controller_data['training_steps']
        self.verbose = controller_data['verbose']
        self.data = controller_data['data']

        print(self.env_settings)
        self._set_training_env(self.env_settings)

        model_file = os.path.join(save_dir, 'model')
        self.model = PPO.load(model_file, env=self.training_env)
        
    def predict(self, obs, deterministic=True):
        """
        Get the sub-system's action, given the current environment observation (state)
        """
        action, _states = self.model.predict(obs, deterministic=deterministic)
        return action, _states

    def _set_training_env(self, env_settings):
        self.training_env = Maze(**env_settings)
        self.training_env.set_observation_size(self.observation_width, self.observation_height, self.observation_top)
        self.training_env.agent_start_states = self.init_state
        #self.training_env.goal_states = self.final_state
        self.training_env.sub_task_goal = self.final_state


    def _init_learning_alg(self, verbose=None):
        self.model = PPO("MlpPolicy", 
                    self.training_env, 
                    verbose=verbose,
                    n_steps=512,
                    batch_size=64,
                    gae_lambda=0.95,
                    gamma=0.99,
                    n_epochs=10,
                    ent_coef=0.0,
                    learning_rate=2.5e-3,
                    clip_range=0.2)
        # self.model = DQN("MlpPolicy",
        #                 self.training_env,
        #                 verbose=verbose,
        #                 batch_size=64,
        #                 tau=1,
        #                 gamma=0.99,
        #                 train_freq=2,
        #                 learning_rate=0.05)
        #self.model = A2C("MultiInputPolicy", self.training_env, verbose=verbose)
    
    def eval_performance(self, n_episodes=400, n_steps=100):
        """
        Perform empirical evaluation of the performance of the learned controller.
        """
        success_count = 0
        avg_num_steps = 0
        trials = 0
        total_steps = 0
        num_steps = 0

        rollout_successes = []
        steps = []

        for episode_ind in range(n_episodes):
            trials = trials + 1

            obs = self.training_env.reset()
            num_steps = 0
            for step_ind in range(n_steps):
                num_steps = num_steps + 1
                total_steps = total_steps + 1
                action, _states = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.training_env.step(action)
                if step_ind == n_steps - 1:
                    rollout_successes.append(0)
                if done:
                    if info['task_complete']:
                        #avg_num_steps = (avg_num_steps + num_steps) / 2
                        steps.append(num_steps)
                        success_count = success_count + 1
                        rollout_successes.append(1)
                    else:
                        rollout_successes.append(0)
                    break
        avg_num_steps = 0
        std_num_steps = 0
        if len(steps) > 0:
            avg_num_steps = np.mean(steps)
            std_num_steps = np.std(steps)
            

        self.data['performance_estimates'] = {
            'training_steps' : self.training_steps,
            'success_count' : success_count,
            'success_rate' : success_count / trials,
            'num_trials' : trials,
            'avg_num_steps' : avg_num_steps,
            'std_num_steps' : std_num_steps
        }

    def get_performance(self):
        return self.data

    def get_data(self):
        data = self.data['performance_estimates']
        return data['success_rate'], data ['avg_num_steps'], data['std_num_steps']

    def demonstrate_capabilities(self, n_episodes=8, n_steps=100, render=True):
        """
        Demonstrate the capabilities of the learned controller in the environment used to train it.
        """
        for episode_ind in range(n_episodes):
            obs = self.training_env.reset()
            self.training_env.render(highlight=False)
            for step in range(n_steps):
                action, _states = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.training_env.step(action)
                if render:
                    self.training_env.render(highlight=False)
                if done:
                    print(info)
                    break

        obs = self.training_env.reset()
        return info['task_complete']

    def is_subtask_complete(self, obs):
        return
    
