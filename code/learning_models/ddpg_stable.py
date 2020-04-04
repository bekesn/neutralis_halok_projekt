import numpy as np

from stable_baselines.ddpg.policies import MlpPolicy
from stable_baselines.common.noise import NormalActionNoise, OrnsteinUhlenbeckActionNoise, AdaptiveParamNoiseSpec
from stable_baselines import DDPG


def training(env):
    # the noise objects for DDPG
    n_actions = env.action_space.shape[-1]
    param_noise = None
    action_noise = OrnsteinUhlenbeckActionNoise(mean=np.zeros(n_actions), sigma=float(0.5) * np.ones(n_actions))

    model = DDPG(MlpPolicy, env, verbose=1, param_noise=param_noise, action_noise=action_noise,render=True,
                 return_range=[-1.0, 1.0],observation_range=[-4.0, 300])
    model.learn(total_timesteps=40000)
    model.save("weights\\ddpg_sb")

    del model # remove to demonstrate saving and loading

    model = DDPG.load("weights\\ddpg_sb")

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render()