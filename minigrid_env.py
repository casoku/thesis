import json
from random import random, randint
from gym_minigrid.minigrid import *
from gym_minigrid.window import Window
import numpy as np
from operator import add

from torch import equal

class Maze(MiniGridEnv):
    """
    Maze environment

    This environment is fully observable
    The state is (x, y, dir) where x,y indicate
    the agent's location in the environment.
    """

    class Actions(IntEnum):
            up = 0
            right = 1
            down = 2
            left = 3

    def __init__(self, agent_start_states = [1, 1], goal_states = [18, 18], observation_width = 20, observation_height = 20, observation_top = [0, 0],slip_p = 0.0, width = 20, height = 20, obstacles_per_room = 1):
        """
        inputs:
        - agent_start_state; 
        - slip_p; chance that the agent accidently takes a ramdom action
        - width; width of the maze
        - height; heigth of the maze
        """

        self.width = width
        self.height = height
        self.observation_width = observation_width
        self.observation_height = observation_height
        self.observation_top = observation_top
        self.size = max(width, height)
        self.agent_start_states = agent_start_states
        self.obstacles_per_room = obstacles_per_room
        self.goal_states = goal_states
        self.sub_task_goal = goal_states
        self.agent_start_dir = 0 # Minigrid requires a direction, however it is not used. 

        super().__init__(grid_size = self.size, max_steps = 4 * self.size * self.size,)

        #Action enumeration for this environment
        self.actions = Maze.Actions

        # Actions are discrete integer values
        self.action_space = spaces.Discrete(len(self.actions))

        #Set observation size
        self.observation_space = spaces.Box(low = 0, high = 5, shape=((self.observation_width * self.observation_height), ), dtype='uint8')
        self.slip_p = slip_p

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

        # Generate the rooms
        num_rooms_in_width = 2
        for i in range(0, num_rooms_in_width):
            for j in range(0, num_rooms_in_width):
                self.grid.wall_rect(j*6, i*6, 7, 7)

        # Add doors
        # Horizontal doors
        for i in range(0, num_rooms_in_width):
            for j in range(0, num_rooms_in_width - 1):
                self.put_obj(Door('grey', is_open=True), (i*6) + 3, (j*6) + 6)
                self.put_obj(Door('grey', is_open=True), (j*6) + 6, (i*6) + 3)
                
        # Place a goal square
        goal_state = self.goal_states
        self.put_obj(Goal(), goal_state[0], goal_state[1])

        # Place the agent
        if self.agent_start_states:
            agent_start_state = self.agent_start_states
            self.agent_pos = (agent_start_state[0], agent_start_state[1])
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        # Place obstacles
        self.obstacles = []
        num_rooms_in_width = 2
        for i in range(0, num_rooms_in_width):
            for j in range(0, num_rooms_in_width):
                self.obstacles.append(Ball())
                self.place_obj(obj = self.obstacles[i * num_rooms_in_width + j], top = (i * 6, j * 6), size = (5, 5), max_tries=100)

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

        #Set observation (size = 4)
        # agentPos = self.agent_pos
        # obstaclePos = self.obstacles[0].cur_pos
        # obs_out = [agentPos[0], agentPos[1], obstaclePos[0], obstaclePos[1]]
        
        
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

    def equal_position(self, pos1, pos2):
        return pos1[0] == pos2[0] and pos1[1] == pos2[1]

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
            while(self.equal_position(old_pos, new_pos) and cur_iteration < max_iterations):
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
        
        # Move forward
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
            if self.equal_position(agent_old_pos, objects_new_pos[i]) and self.equal_position(agent_new_pos, objects_old_pos[i]):
                collision = True
            

        if agent_new_cell == None or agent_new_cell.can_overlap():
            self.agent_pos = agent_new_pos
        #if agent_new_cell != None and agent_new_cell.type == 'goal':
        if self.equal_position(agent_new_pos, self.sub_task_goal):
            #print(agent_new_cell.type)
            done = True
            info['task_complete'] = True
            reward = 1
        if (agent_new_cell != None and agent_new_cell.type == 'ball') or collision:
            #print(agent_new_cell.type)
            done = True
            info['ball'] = True
            reward = -1
        if agent_new_cell != None and agent_new_cell.type == 'wall':
            #print(agent_new_cell.type)
            done = True
            info['wall'] = True
            reward = -1
        
        obs = self.gen_obs()

        #print(obs)
        return obs, reward, done, info
