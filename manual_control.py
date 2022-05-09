#!/usr/bin/env python3

from enum import IntEnum
import argparse
import numpy as np
from gym_minigrid.wrappers import *
from gym_minigrid.window import Window
from Environment import Environment
from Environment_simple import Environment_simple
from Environment_test import Environment_test

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
    print(obs)
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

# %% Setup and create the environment
# goal_state = [7, 7] # The final goal state to reach in the complex environment
# start_state = [1,1]

# env_settings = {
#     'agent_start_states' : start_state,
#     'goal_states': goal_state,
#     'slip_p' : 0,
#     'width' : 8,
#     'height' : 8
# }
# env = Environment_test(**env_settings)

env_settings = {
    'agent_start_states' : [1, 1],
    'goal_states': [13, 13],
    'slip_p' : 0,
    'width' : 15,
    'height' : 15
}
env = Environment_simple(**env_settings)

observation_top = [0, 0]
observation_width = 8
observation_height = 8
env.sub_task_goal = [7, 4]
env.set_observation_size(observation_width, observation_height, observation_top)

window = Window('gym_minigrid - Maze')
window.reg_key_handler(key_handler)

reset()

# Blocking event loop
window.show(block=True)
