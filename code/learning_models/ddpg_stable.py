import numpy as np

from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
from stable_baselines import DDPG
from datetime import datetime

def training(env):
    n_actions = env.action_space.shape[-1]
    param_noise = None
    action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=float(0.5) * np.ones(n_actions))

    model = DDPG(MlpPolicy, env, verbose=1, param_noise=param_noise, action_noise=action_noise, render=True,
                 return_range=[-1.0, 1.0],observation_range=[-2.0, 2.0])
    model.learn(total_timesteps=40000)
    time=datetime.now().strftime("%m%d_%H%M%S")
    model.save("models\\ddpg_sbl_"+time)

    del model # remove to demonstrate saving and loading
    testing(env, time)

def testing(env,name):
    model = DDPG.load("models\\ddpg_sbl_"+name)

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, done, info = env.step(action)
        env.render()
        if done or env.steps>1000:
            env.reset()