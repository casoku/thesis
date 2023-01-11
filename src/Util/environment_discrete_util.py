import collections
import random
#from dijkstar import Graph, find_path
from gym_minigrid.minigrid import *
from operator import add

def same_position(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def generate_rooms(grid=None):
    assert grid is not None

    num_rooms_in_width = 2
    for i in range(0, num_rooms_in_width):
        for j in range(0, num_rooms_in_width):
            grid.wall_rect(j*7, i*7, 8, 8)

def generate_walls(grid=None):
    #room1
    grid.wall_rect(2, 0, 1, 3) 
    grid.wall_rect(0, 4, 6, 1)   
    grid.wall_rect(5, 3, 1, 2)   

    #room2
    grid.wall_rect(9, 5, 6, 1)
    grid.wall_rect(11, 0, 1, 4)

    #room3
    grid.wall_rect(5, 8, 1, 5)
    grid.wall_rect(2, 12, 3, 1) 

    #room4
    grid.wall_rect(12, 8, 1, 5)
    grid.wall_rect(10, 9, 1, 5)

def generate_doors(environment=None):
    assert environment is not None

    num_rooms_in_width = 2
    for i in range(0, num_rooms_in_width):
        for j in range(0, num_rooms_in_width - 1):
            environment.put_obj(Door('grey', is_open=True), (i*7) + 3, (j*7) + 7)
            environment.put_obj(Door('grey', is_open=True), (j*7) + 7, (i*7) + 3)

def place_goal(environment=None):
    assert environment is not None

    for goal_state in environment.goal_states:
        goal = Goal()
        goal.color = goal_state['color']
        goal_location = goal_state['state']
        environment.put_obj(goal, goal_location[0], goal_location[1])

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

    num_rooms_in_width = 3
    for i in range(0, num_rooms_in_width):
        for j in range(0, num_rooms_in_width):
            environment.obstacles.append(Ball())
            environment.place_obj(obj = environment.obstacles[i * num_rooms_in_width + j], top = (i * 7, j * 7), size = (6, 6), max_tries=100)

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
    
    # Add agent to observation
    if agent_pos[1] - environment.observation_top[1] < obs_grid.height and agent_pos[1] - environment.observation_top[1] >= 0 and agent_pos[0] - environment.observation_top[0] < obs_grid.width and agent_pos[0] - environment.observation_top[0] >= 0:
        obs_out[(agent_pos[1] - environment.observation_top[1]) * obs_grid.width + agent_pos[0] - environment.observation_top[0]] = 'agent'
    
    #Add goal to observation
    if environment.sub_task_goal[0] < obs_grid.width and environment.sub_task_goal[1] < obs_grid.height:
        obs_out[environment.sub_task_goal[1] * obs_grid.width + environment.sub_task_goal[0]] = 'goal'
    #print(obs_out)
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

def gen_dijkstra_graph(environment, start, end):
    obs_out = environment.gen_obs()
    grid = np.array(obs_out)  
    grid = np.reshape(grid, (environment.observation_height, environment.observation_width))
    
    height = len(grid)
    width = len(grid[0])

    agent_x = start[0] - environment.observation_top[0]
    agent_y = start[1] - environment.observation_top[1]
    start_corrected_pos = (agent_x, agent_y)
    #print("start location: " + str(start_corrected_pos))
    
    end_x = end[0] - environment.observation_top[0]
    end_y = end[1] - environment.observation_top[1]
    end_corrected_pos = (end_x, end_y)
    #print("end location: " + str(end_corrected_pos))
    graph = Graph(undirected=True)

    #print(grid)
    for y in range(height):
        for x in range(width):
            for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != 1 and grid[y2][x2] != 3 and grid[y][x] != 1 and grid[y][x] != 3:
                    node1 = str(x) + "_" + str(y)
                    node2 = str(x2) + "_" + str(y2)
                   # print("id: " + str(node2)+ " cell: " + str(grid[y2][x2]))
                    graph.add_edge(node1, node2, 1)

    start_id = str(start[0]) + "_" + str(start[1])
    end_id = str(end[0]) + "_" + str(end[1])
    corrected_start_id = str(start_corrected_pos[0]) + "_" + str(start_corrected_pos[1])
    corrected_end_id = str(end_corrected_pos[0]) + "_" + str(end_corrected_pos[1])
    # print("start id: " + start_id)
    # print("end id: " + end_id)
    # print("corrected start id: " + corrected_start_id)
    # print("corrected end id: " + corrected_end_id)

    if  start_corrected_pos[0] < 0 or start_corrected_pos[0] >= width or start_corrected_pos[1] < 0 or start_corrected_pos[1] >= height:
        return 0

    if  end_corrected_pos[0] < 0 or end_corrected_pos[0] >= width or end_corrected_pos[1] < 0 or end_corrected_pos[1] >= height:
        return 0

    #print(find_path(graph, corrected_start_id, corrected_end_id))

    return find_path(graph, corrected_start_id, corrected_end_id)

def update_environment(environment=None, objects_old_pos=None, objects_new_pos=None, agent_old_pos=None, agent_new_pos=None, agent_new_cell=None):
    assert environment is not None

    done = False

    reward = -0.03

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
    
    agent_pos = environment.agent_pos
    obs_grid = environment.grid.slice(environment.observation_top[0], environment.observation_top[1], environment.observation_width, environment.observation_height)
    if not(agent_pos[1] - environment.observation_top[1] < obs_grid.height and agent_pos[1] - environment.observation_top[1] >= 0 and agent_pos[0] - environment.observation_top[0] < obs_grid.width and agent_pos[0] - environment.observation_top[0] >= 0):
        done = True
        reward = -10
        return done, info, reward
        
    if agent_new_cell == None or agent_new_cell.can_overlap():
        # old_distance_to_goal = gen_dijkstra_graph(environment, agent_old_pos, environment.sub_task_goal)
        # new_distance_to_goal = gen_dijkstra_graph(environment, agent_new_pos, environment.sub_task_goal)
        # #generate reward based on shortest path 
        # #reward = dijkstra_reward(environment)
        # # print("agent_old_pos: " + str(agent_old_pos))
        # # print("agent_new_pos: " + str(agent_new_pos))

        # if(new_distance_to_goal < old_distance_to_goal):
        #    reward = 0.3
        #    #print("closer!")
        # else:
        #    reward = -0.2

        # #reward = (10 - new_distance_to_goal)

        environment.agent_pos = agent_new_pos
    if same_position(agent_new_pos, environment.sub_task_goal):
        print("task complete!")
        done = True
        info['task_complete'] = True
        reward = 100
    if (agent_new_cell != None and agent_new_cell.type == 'ball') or collision:
        done = True
        info['ball'] = True
        reward = -1
    if agent_new_cell != None and agent_new_cell.type == 'lava':
        done = True
        info['lava'] = True
        #reward = -1
    # if agent_new_cell != None and agent_new_cell.type == 'wall':
    #     reward = -0.1

    #print("reward: " + str(reward))
    return done, info, reward

