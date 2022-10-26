#!/usr/bin/env python3

from enum import IntEnum
import argparse
import numpy as np
from gym_minigrid.wrappers import *
from gym_minigrid.window import Window
from Environment import Environment
from Environment_9_rooms import Environment_9_rooms
from Environment_simple import Environment_simple
from Environment_test import Environment_test
from Environment_discrete import Environment_discrete_rooms

class Actions(IntEnum):
        up = 0
        right = 1
        down = 2
        left = 3

actions = Actions

def redraw(img):
    img = env.render('rgb_array', highlight = False, tile_size=args.tile_size)
    window.show_img(img)

def reset():
    if args.seed != -1:
        env.seed(args.seed)

    obs = env.reset()

    if hasattr(env, 'mission'):
        print('Mission: %s' % env.mission)
        window.set_caption(env.mission)

    redraw(obs)

def step(action):
    obs, reward, done, info = env.step(action)
    #print(obs)
    print('step=%s, reward=%.2f' % (env.step_count, reward))

    if done:
        print('done!')
        reset()
    else:
        redraw(obs)

def key_handler(event):
    print('pressed', event.key)

    if event.key == 'escape':
        window.close()
        return

    if event.key == 'backspace':
        reset()
        return

    if event.key == 'left':
        step(actions.left)
        return
    if event.key == 'right':
        step(actions.right)
        return
    if event.key == 'up':
        step(actions.up)
        return
    if event.key == 'down':
        step(actions.down)

    # Spacebar
    if event.key == ' ':
        step(env.actions.toggle)
        return
    if event.key == 'pageup':
        step(env.actions.pickup)
        return
    if event.key == 'pagedown':
        step(env.actions.drop)
        return

    if event.key == 'enter':
        step(env.actions.done)
        return

parser = argparse.ArgumentParser()
parser.add_argument(
    "--seed",
    type=int,
    help="random seed to generate the environment with",
    default=-1
)
parser.add_argument(
    "--tile_size",
    type=int,
    help="size at which to render tiles",
    default=32
)

args = parser.parse_args()

# goal_state = [13, 13] # The final goal state to reach in the complex environment
# goal_1 = {'state': [1, 1], 'color': 'green'}
# goal_3 = {'state': [1, 2], 'color': 'green'}
# goal_4 = {'state': [2, 1], 'color': 'green'}
# goal_5 = {'state': [2, 2], 'color': 'green'}
# goal_2 = {'state': [1, 6], 'color': 'purple'}
# goal_6 = {'state': [1, 5], 'color': 'purple'}
# goal_7 = {'state': [2, 6], 'color': 'purple'}
# goal_8 = {'state': [2, 5], 'color': 'purple'}
# goal_states = []
# goal_states.append(goal_1)
# goal_states.append(goal_2)
# goal_states.append(goal_3)
# goal_states.append(goal_4)
# goal_states.append(goal_5)
# goal_states.append(goal_6)
# goal_states.append(goal_7)
# goal_states.append(goal_8)
# start_state = [7,3]

# env_settings = {
#     'agent_start_states' : [3, 7],
#     'goal_states': goal_states,
#     'slip_p' : 0,
#     'width' : 15,
#     'height' : 15
# }
# env = Environment_test(**env_settings)


goal_state = [13, 13] # The final goal state to reach in the complex environment
goal_1 = {'state': [13, 13], 'color': 'green'}
goal_2 = {'state': [13, 1], 'color': 'purple'}
goal_states = []
goal_states.append(goal_1)
goal_states.append(goal_2)
start_state = [1,1]

env_settings = {
    'agent_start_states' : [1, 1],
    'goal_states': goal_states,
    'slip_p' : 0,
    'width' : 15,
    'height' : 15
}
env = Environment_simple(**env_settings)



# start_state = [1,1]
# goal_1 = {'state': [20, 20], 'color': 'green'}
# goal_2 = {'state': [1, 20], 'color': 'purple'}
# goal_3 = {'state': [20, 6], 'color': 'yellow'}
# goal_4 = {'state': [10, 10], 'color': 'cyan'}
# goal_states = []
# goal_states.append(goal_1)
# goal_states.append(goal_2)
# goal_states.append(goal_3)
# goal_states.append(goal_4)

# '''
# Create environment in which the high-level-controller will be tested
# '''
# env_settings = {
#     'agent_start_states' : start_state,
#     'goal_states': goal_states,
#     'slip_p' : 0,
#     'width' : 22,
#     'height' : 22
# }
# env = Environment_9_rooms(**env_settings)


window = Window('gym_minigrid - Maze')
window.reg_key_handler(key_handler)

reset()

# Blocking event loop
window.show(block=True)
