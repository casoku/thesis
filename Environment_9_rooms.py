import json
from random import randint
from gym_minigrid.minigrid import *
import numpy as np

from Util.environment_9_rooms_util import *

class Environment_9_rooms(MiniGridEnv):
    """
    Grid Environment

    This environment is fully observable
    The observation is an array off all cells within a sub-section of the entire grid 
    """

    class Actions(IntEnum):
            up = 0
            right = 1
            down = 2
            left = 3

    def __init__(self, agent_start_states=[1, 1], goal_states=[18, 18], observation_width=20, observation_height=20, observation_top=[0, 0],slip_p=0.0, width=20, height=20, obstacles_per_room=1):
        self.width = width
        self.height = height
        self.size = width* height
        self.agent_start_states = agent_start_states
        self.obstacles_per_room = obstacles_per_room
        self.obstacles = []
        self.goal_states = goal_states
        self.sub_task_goal = goal_states
        self.agent_start_dir = 0 # Minigrid requires a direction, however it is not used. 

        #Set observation size
        self.set_observation_size(observation_width, observation_height, observation_top)
        self.slip_p = slip_p    #Not used

        super().__init__(width=self.width, height=self.height, max_steps=4 * self.size)

        #Action enumeration for this environment
        self.actions = Environment_9_rooms.Actions

        # Actions are discrete integer values
        self.action_space = spaces.Discrete(len(self.actions))

    def set_observation_size(self, observation_width, observation_height, observation_top):
        self.observation_width = observation_width
        self.observation_height = observation_height
        self.observation_top = observation_top

        self.observation_space = spaces.Box(low = 0, high = 5, shape=((self.observation_width * self.observation_height), ), dtype='uint8')

    def _gen_grid(self, width, height):
        #Generate new seed, so that the map has randomized obstacle positions
        seed = randint(0, 2000)
        self.seed(seed)

        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        generate_rooms(self.grid)
        generate_doors(self)

        place_goal(self)
        place_agent(self)
        place_obstacles(self)

        self.mission = "get to the green goal square"

    def gen_obs(self):
        """
        Generate the observation of the agent, which in this environment, is its state.
        """
        obs_grid, obs_out = create_observation(self)

        #change observation to integers
        with open('map_obs.json') as json_file:
            data = json.load(json_file)
            map = data['map']

            for i in range (obs_grid.height * obs_grid.width):
                obs_out[i] = map[obs_out[i]]
               
        return obs_out

    def get_front_pos(self, action):
        """
        Get the cell in front of the agent based on the action it executes
        """
        front_pos = None

        if action == self.actions.up:
            front_pos = np.add(self.agent_pos,  np.array([0, -1]))
            
        if action == self.actions.right:
            front_pos = np.add(self.agent_pos,  np.array([1, 0]))

        if action == self.actions.down:
            front_pos = np.add(self.agent_pos,  np.array([0, 1]))

        if action == self.actions.left:
            front_pos = np.add(self.agent_pos,  np.array([-1, 0]))

        return front_pos

    def step(self, action):
        """
        Update the environment with obstacle and agent movement
        """
        self.step_count += 1

        # Invalid action
        if action >= self.action_space.n:
            action = 0

        # Update obstacle positions
        objects_old_pos, objects_new_pos = update_obstacles_positions(self)
        
        # Update the agent's position
        agent_old_pos = self.agent_pos
        agent_new_pos = self.get_front_pos(action)
        agent_new_cell = self.grid.get(*agent_new_pos)

        done, info, reward = update_environment(self, objects_old_pos, objects_new_pos, agent_old_pos, agent_new_pos, agent_new_cell)
        
        obs = self.gen_obs()

        return obs, reward, done, info
