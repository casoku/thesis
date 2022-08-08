import gym
from Environment_simple import Environment_simple
from Environment_test import Environment_test
from Util.Objective import Objective
from Environment import Environment
from Environment_discrete import Environment_discrete_rooms
from subtask_controller import SubtaskController

# goal_1 = {'state': [1, 6], 'color': 'green'}
# goal_2 = {'state': [13, 1], 'color': 'yellow'}
# goal_3 = {'state': [13, 8], 'color': 'purple'}
# goal_states = []
# goal_states.append(goal_1)
# goal_states.append(goal_2)
# goal_states.append(goal_3)
# start_state = [1,1]
# goal_state = [13,13]
# '''
# Create environment in which the high-level-controller will be tested
# '''
# env_settings = {
#     'agent_start_states' : start_state,
#     'goal_states': goal_states,
#     'slip_p' : 0,
#     'width' : 15,
#     'height' : 15
# }
# env = Environment_discrete_rooms(**env_settings)

goal_1 = {'state': [13, 13], 'color': 'green'}
goal_2 = {'state': [13, 1], 'color': 'purple'}
goal_states = []
goal_states.append(goal_1)
goal_states.append(goal_2)
start_state = [1,1]
goal_state = [13,13]
'''
Create environment in which the high-level-controller will be tested
'''
env_settings = {
    'agent_start_states' : start_state,
    'goal_states': goal_states,
    'slip_p' : 0,
    'width' : 15,
    'height' : 15
}

env = Environment_simple(**env_settings)

controller_list = []
controller_id = -1

def assign_controller_id(controller_id):
    controller_id += 1
    return controller_id

# #--------First room controllers--------
# initial_state = [1,1]
# goal_state = [7,3]
# observation_top = [0, 0]
# observation_width = 8
# observation_height = 8
# #final_states = [11, 11]
# task1 = Objective(initial_state, goal_state, observation_top, observation_width, observation_height)
# controller = SubtaskController(assign_controller_id(controller_id), task1.start_state, task1.goal_state, env=env, verbose=1,
#                 observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
# controller.learn(15000)
# controller.save("test_subcontroller1")

# initial_states2 = [1,1]
# final_states2 = [3,7] #(x, y, orientation)
# task2 = Objective(initial_states2, final_states2, observation_top, observation_width, observation_height)
# controller2 = SubtaskController(assign_controller_id(controller_id), task2.start_state, task2.goal_state, env=env, verbose=1,
#                 observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
# controller2.learn(15000)
# controller2.save("test_subcontroller2")

# #--------Second room controllers--------
# initial_states3 = [6,3]
# final_states3 = [9,6]
# observation_top = [6, 0]
# task3 = Objective(initial_states3, final_states3, observation_top, observation_width, observation_height)
# controller3 = SubtaskController(assign_controller_id(controller_id), task3.start_state, task3.final_state, env_settings=env_settings,
#                 observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
# controller3.learn()

# #--------Third room controllers--------
# initial_states4 = [3, 6]
# final_states4 = [6,9]
# observation_top = [0, 6]
# task4 = Objective(initial_states4, final_states4, observation_top, observation_width, observation_height)
# controller4 = SubtaskController(assign_controller_id(controller_id), task4.start_state, task4.final_state, env_settings=env_settings,
#                 observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
# controller4.learn()

# #--------Fourth room controllers--------
# initial_states5 = [9, 6]
# final_states5 = [11,11]
# observation_top = [6, 6]
# task5 = Objective(initial_states5, final_states5, observation_top, observation_width, observation_height)
# controller5 = SubtaskController(assign_controller_id(controller_id), task5.start_state, task5.final_state, env_settings=env_settings,
#                 observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
# controller5.learn()

# initial_states6 = [6, 9]
# final_states6 = [11,11]
# observation_top = [6, 6]
# task6 = Objective(initial_states6, final_states6, observation_top, observation_width, observation_height)
# controller6 = SubtaskController(assign_controller_id(controller_id), task6.start_state, task6.final_state, env_settings=env_settings,
#                 observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
# controller6.learn()

task14 = Objective([1,1], [3,7], [0,0], 8, 8)
controller14 = SubtaskController(controller_id, task14.start_state, task14.goal_state, env=env, verbose=1,
                 observation_top=task14.observation_top, observation_width=task14.observation_width, observation_height=task14.observation_height)
controller14.learn(50000)
controller14.save("test_subcontroller14_v2")
del controller14.model
print("-------------Controller 14 performance----------------------")
controller14 = None
controller14 = SubtaskController(load_dir="test_subcontroller14_v2")
controller14.eval_performance(600)
performance = controller14.get_performance()
print(performance)
controller14.demonstrate_capabilities(n_episodes=2)
print()

# print("-------------Controller 1 performance----------------------")
# controller = None
# controller = SubtaskController(load_dir="test_subcontroller1")
# controller.eval_performance(100)
# performance = controller.get_performance()
# print(performance)
# controller.demonstrate_capabilities()
# print()
# print("-------------Controller 2 performance----------------------")
# controller2 = None
# controller2 = SubtaskController(load_dir="test_subcontroller2")
# controller2.eval_performance(100)
# performance = controller2.get_performance()
# print(performance)
# controller2.demonstrate_capabilities()
# print("-------------Controller 3 performance----------------------")
# controller3.eval_performance()
# performance = controller3.get_performance()
# print(performance)
# print(performance['performance_estimates']['avg_num_steps'])
# if(performance['performance_estimates']['avg_num_steps'] > 10):
#     controller.demonstrate_capabilities()
# print()
# print("-------------Controller 4 performance----------------------")
# controller4.eval_performance()
# performance = controller4.get_performance()
# print(performance)
# print(performance['performance_estimates']['avg_num_steps'])
# if(performance['performance_estimates']['avg_num_steps'] > 10):
#     controller.demonstrate_capabilities()
# print()
# print("-------------Controller 5 performance----------------------")
# controller5.eval_performance()
# performance = controller5.get_performance()
# print(performance)
# print(performance['performance_estimates']['avg_num_steps'])
# if(performance['performance_estimates']['avg_num_steps'] > 10):
#     controller.demonstrate_capabilities()
# print()
# print("-------------Controller 6 performance----------------------")
# controller6.eval_performance()
# performance = controller6.get_performance()
# print(performance)
# print(performance['performance_estimates']['avg_num_steps'])
# if(performance['performance_estimates']['avg_num_steps'] > 10):
#     controller.demonstrate_capabilities()
# print()


# import gym
# from gym_minigrid.wrappers import *
# from stable_baselines3 import DQN, PPO
# from stable_baselines3.common.evaluation import evaluate_policy


# # Create environment
# env = gym.make('MiniGrid-FourRooms-v0')
# env = RGBImgPartialObsWrapper(env) # Get pixel observations
# env = ImgObsWrapper(env) # Get rid of the 'mission' field

# # Instantiate the agent
# model = PPO('MlpPolicy', env, learning_rate=1e-3, verbose=1)
# # Train the agent
# model.learn(total_timesteps=int(1e6))
# # Save the agent
# model.save("four_rooms")
# del model  # delete trained model to demonstrate loading

# # Load the trained agent
# model = PPO.load("four_rooms")

# # Evaluate the agent
# #mean_reward, std_reward = evaluate_policy(model, model.get_env(), n_eval_episodes=10)

# # Enjoy trained agent
# obs = env.reset()
# for i in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()