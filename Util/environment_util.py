from gym_minigrid.minigrid import *

def same_position(pos1, pos2):
    return pos1[0] == pos2[0] and pos1[1] == pos2[1]

def generate_rooms(grid=None):
    assert grid is not None

    num_rooms_in_width = 2
    for i in range(0, num_rooms_in_width):
        for j in range(0, num_rooms_in_width):
            grid.wall_rect(j*6, i*6, 7, 7)

def generate_doors(environment=None):
    assert environment is not None

    num_rooms_in_width = 2
    for i in range(0, num_rooms_in_width):
        for j in range(0, num_rooms_in_width - 1):
            environment.put_obj(Door('grey', is_open=True), (i*6) + 3, (j*6) + 6)
            environment.put_obj(Door('grey', is_open=True), (j*6) + 6, (i*6) + 3)

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
