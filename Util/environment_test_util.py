import random
from turtle import width
from gym_minigrid.minigrid import *
from operator import add

def same_position(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def generate_rooms(grid=None):
    assert grid is not None

    #generate wall room 1
    grid.horz_wall(4,2,2)
    grid.vert_wall(5,2,2)
    grid.horz_wall(2,5,2)
    grid.vert_wall(2,4,2)

def generate_doors(environment=None):
    assert environment is not None

    environment.put_obj(Door('grey', is_open=True), 4, 7)
    environment.put_obj(Door('grey', is_open=True), 7, 4)

def place_goal(environment=None):
    assert environment is not None

    goal_state = environment.goal_states
    environment.put_obj(Goal(), goal_state[0], goal_state[1])

def place_agent(environment=None):
    assert environment is not None

    if environment.agent_start_states:
        agent_start_state = environment.agent_start_states
        environment.agent_pos = (agent_start_state[0], agent_start_state[1])
        environment.agent_dir = environment.agent_start_dir
    else:
        environment.place_agent()

def place_obstacles(environment=None):
    assert environment is not None

    environment.obstacles = []
    num_rooms_in_width = 2
    for i in range(0, num_rooms_in_width):
        for j in range(0, num_rooms_in_width):
            environment.obstacles.append(Ball())
            environment.place_obj(obj = environment.obstacles[i * num_rooms_in_width + j], top = (i * 6, j * 6), size = (5, 5), max_tries=100)

def create_observation(environment=None):
    assert environment is not None

    agent_pos = environment.agent_pos
    obs_grid = environment.grid.slice(environment.observation_top[0], environment.observation_top[1], environment.observation_width, environment.observation_height)
    #obs_grid = self.grid

    def map_fun(object):
        if (object == None):
            return "none"
        else:
            return object.type

    obs_out = [map_fun(line) for line in obs_grid.grid] 
    
    #Add sub goal to observation
    #print(environment.sub_task_goal)
    if environment.sub_task_goal[1] - environment.observation_top[1] < obs_grid.height and environment.sub_task_goal[1] - environment.observation_top[1] >= 0 and environment.sub_task_goal[0] - environment.observation_top[0] < obs_grid.width and environment.sub_task_goal[0] - environment.observation_top[0] >= 0:
        obs_out[(environment.sub_task_goal[1] - environment.observation_top[1]) * obs_grid.width + environment.sub_task_goal[0] - environment.observation_top[0]] = 'goal'

    # Add agent to observation
    if agent_pos[1] - environment.observation_top[1] < obs_grid.height and agent_pos[1] - environment.observation_top[1] >= 0 and agent_pos[0] - environment.observation_top[0] < obs_grid.width and agent_pos[0] - environment.observation_top[0] >= 0:
        obs_out[(agent_pos[1] - environment.observation_top[1]) * obs_grid.width + agent_pos[0] - environment.observation_top[0]] = 'agent'

    return obs_grid, obs_out

def update_obstacles_positions(environment=None):
    assert environment is not None

    objects_old_pos = []
    objects_new_pos = []
    for i_obst in range(len(environment.obstacles)):
        old_pos = environment.obstacles[i_obst].cur_pos
        objects_old_pos.append(old_pos)
        new_pos = old_pos
        
        #Generate new coordinate for obstacles, ensure it makes a move if possible
        max_iterations = 50
        cur_iteration = 0 
        while(same_position(old_pos, new_pos) and cur_iteration < max_iterations):
            x_or_y = random.random()
            change_array = [-1, 1]
            change = change_array[random.randint(0, 1)]
            if x_or_y < 0.5:
                top = tuple(map(add, old_pos, (change, 0)))
            else:
                top = tuple(map(add, old_pos, (0, change)))
            cur_iteration += 1

            try:
                new_pos = environment.place_obj(environment.obstacles[i_obst], top=top, size=(1,1), max_tries=10)
                environment.grid.set(*old_pos, None)
            except:
                pass
        
        objects_new_pos.append(new_pos)

    return objects_old_pos, objects_new_pos

def update_environment(environment=None, objects_old_pos=None, objects_new_pos=None, agent_old_pos=None, agent_new_pos=None, agent_new_cell=None):
    assert environment is not None

    done = False
    reward = -0.01

    info = {
        'task_complete' : False,
        'ball' : False,
        'lava' : False
    }
    #Check if there is a collision when agent and object swap places
    collision = False
    for i in range(0, len(objects_old_pos)):
        if same_position(agent_old_pos, objects_new_pos[i]) and same_position(agent_new_pos, objects_old_pos[i]):
            collision = True
        

    if agent_new_cell == None or agent_new_cell.can_overlap():
        environment.agent_pos = agent_new_pos
    if same_position(agent_new_pos, environment.sub_task_goal):
        done = True
        info['task_complete'] = True
        reward = 1
    if (agent_new_cell != None and agent_new_cell.type == 'ball') or collision:
        done = True
        info['ball'] = True
        reward = -1
    if agent_new_cell != None and agent_new_cell.type == 'lava':
        done = True
        info['lava'] = True
        reward = -1

    return done, info, reward

