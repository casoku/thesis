import gym
from Environment_deterministic import Deterministic_Environment
from Environment_test import Environment_test
from Util.Objective import Objective
from Environment import Environment
from subtask_controller import SubtaskController

# env_settings = {
#     'agent_start_states' : [1,1],
#     'goal_states': [11, 11],
#     'slip_p' : 0,
#     'width' : 13,
#     'height' : 13
# }
# env = Environment(**env_settings)
#env = gym.make('MiniGrid-FourRooms-v0')

env_settings = {
    'agent_start_states' : [1, 1],
    'goal_states': [7, 7],
    'slip_p' : 0,
    'width' : 8,
    'height' : 8
}
env = Environment_test(**env_settings)

# '''
# Create environment in which the high-level-controller will be tested
# '''
# env_settings = {
#     'agent_start_states' : [1,1],
#     'goal_states': [2, 24],
#     'slip_p' : 0,
#     'width' : 29,
#     'height' : 29,
#     'obstacles_per_room': 0
# }
# env = Deterministic_Environment(**env_settings)

controller_list = []
controller_id = -1

def assign_controller_id(controller_id):
    controller_id += 1
    return controller_id

# #--------First room controllers--------
initial_state = [1,1]
goal_state = [7,4]
observation_top = [0, 0]
observation_width = 8
observation_height = 8
#final_states = [11, 11]
task1 = Objective(initial_state, goal_state, observation_top, observation_width, observation_height)
controller = SubtaskController(assign_controller_id(controller_id), task1.start_state, task1.goal_state, env=env, verbose=1,
                observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
controller.learn(15000)
controller.save("test_subcontroller1")

initial_states2 = [1,1]
final_states2 = [4,7] #(x, y, orientation)
task2 = Objective(initial_states2, final_states2, observation_top, observation_width, observation_height)
controller2 = SubtaskController(assign_controller_id(controller_id), task2.start_state, task2.goal_state, env=env, verbose=1,
                observation_top=observation_top, observation_width=observation_width, observation_height=observation_height)
controller2.learn(15000)
controller2.save("test_subcontroller2")

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

print("-------------Controller 1 performance----------------------")
controller = None
controller = SubtaskController(load_dir="test_subcontroller1")
controller.eval_performance(100)
performance = controller.get_performance()
print(performance)
#controller.demonstrate_capabilities()
print()
print("-------------Controller 2 performance----------------------")
controller2 = None
controller2 = SubtaskController(load_dir="test_subcontroller2")
controller2.eval_performance(100)
performance = controller2.get_performance()
print(performance)
#controller2.demonstrate_capabilities()
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