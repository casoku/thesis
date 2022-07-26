import gym
from gym_minigrid.minigrid import *
from stable_baselines3 import PPO
env = gym.make("MontezumaRevenge-v0")
env.reset()

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
print(obs)

episodes = 10

for ep in range(episodes):
    obs = env.reset()
    done = False

    while not done:
        env.render()
        obs, reward, done, info = env.step(model.predict(obs))

env.close()

# print("sample action:", env.action_space.sample())

# print("observation space shape", env.observation_space.shape)
# print("sample observation", env.observation_space.sample())