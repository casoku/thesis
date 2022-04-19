import json
from random import random, randint
from gym_minigrid.minigrid import *
import numpy as np
from operator import add

from Util.environment_util import generate_doors, generate_rooms, place_agent, place_goal, place_obstacles, same_position

class Environment(MiniGridEnv):
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
        self.size = max(width, height)
        self.agent_start_states = agent_start_states
        self.obstacles_per_room = obstacles_per_room
        self.goal_states = goal_states
        self.sub_task_goal = goal_states
        self.agent_start_dir = 0 # Minigrid requires a direction, however it is not used. 

        #Set observation size
        self.set_observation_size(observation_width, observation_height, observation_top)
        self.slip_p = slip_p

        super().__init__(grid_size=self.size, max_steps=4 * self.size * self.size)

        #Action enumeration for this environment
        self.actions = Environment.Actions

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
        
        agent_pos = self.agent_pos
        obs_grid = self.grid.slice(self.observation_top[0], self.observation_top[1], self.observation_width, self.observation_height)
        #obs_grid = self.grid

        def map_fun(object):
            if (object == None):
                return "none"
            else:
                return object.type

        obs_out = [map_fun(line) for line in obs_grid.grid] 
        
        if agent_pos[1] - self.observation_top[1] < obs_grid.height and agent_pos[1] - self.observation_top[1] >= 0 and agent_pos[0] - self.observation_top[0] < obs_grid.width and agent_pos[0] - self.observation_top[0] >= 0:
            obs_out[(agent_pos[1] - self.observation_top[1]) * obs_grid.width + agent_pos[0] - self.observation_top[0]] = 'agent'

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
        objects_old_pos = []
        objects_new_pos = []
        for i_obst in range(len(self.obstacles)):
            old_pos = self.obstacles[i_obst].cur_pos
            objects_old_pos.append(old_pos)
            new_pos = old_pos
            
            #Generate new coordinate for obstacles, ensure it makes a move if possible
            max_iterations = 50
            cur_iteration = 0 
            while(same_position(old_pos, new_pos) and cur_iteration < max_iterations):
                x_or_y = random()
                change_array = [-1, 1]
                change = change_array[randint(0, 1)]
                if x_or_y < 0.5:
                    top = tuple(map(add, old_pos, (change, 0)))
                else:
                    top = tuple(map(add, old_pos, (0, change)))
                cur_iteration += 1

                try:
                    new_pos = self.place_obj(self.obstacles[i_obst], top=top, size=(1,1), max_tries=10)
                    self.grid.set(*old_pos, None)
                except:
                    pass
            
            objects_new_pos.append(new_pos)
        
        # Update the agent's position
        agent_old_pos = self.agent_pos
        agent_new_pos = self.get_front_pos(action)
        agent_new_cell = self.grid.get(*agent_new_pos)

        done = False
        reward = 0

        info = {
            'task_complete' : False,
            'ball' : False,
            'wall' : False
        }
        #Check if there is a collision when agent and object swap places
        collision = False
        for i in range(0, len(objects_old_pos)):
            if same_position(agent_old_pos, objects_new_pos[i]) and same_position(agent_new_pos, objects_old_pos[i]):
                collision = True
            

        if agent_new_cell == None or agent_new_cell.can_overlap():
            self.agent_pos = agent_new_pos
        if same_position(agent_new_pos, self.sub_task_goal):
            done = True
            info['task_complete'] = True
            reward = 1
        if (agent_new_cell != None and agent_new_cell.type == 'ball') or collision:
            done = True
            info['ball'] = True
            reward = -1
        if agent_new_cell != None and agent_new_cell.type == 'wall':
            done = True
            info['wall'] = True
            reward = -1
        
        obs = self.gen_obs()

        return obs, reward, done, info
