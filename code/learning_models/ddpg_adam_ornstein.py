import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory
from rl.random import OrnsteinUhlenbeckProcess
from datetime import datetime

def training(env):
    agent = create_agent(env)

    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    agent.fit(env, nb_steps=16000, action_repetition=1, nb_max_episode_steps=500, visualize=False, verbose=2)

    # After training is done, we save the best weights.
    agent.save_weights('weights\\ddpg'+datetime.now().strftime("%m%d_%H%M%S")+'.h5f', overwrite=True)

    # Finally, evaluate our algorithm for 5 episodes.
    agent.test(env, nb_episodes=5, action_repetition=1, nb_max_episode_steps=2000, visualize=True)

def testing(env, num, date):
    agent=create_agent(env)
    agent.load_weights('weights\\ddpg_'+date+'.h5f')
    agent.test(env, nb_episodes=num, nb_max_episode_steps=2000, visualize=True)


def create_agent(env):
    np.random.seed(123)
    env.seed(None)

    nb_actions = env.action_space.shape[0]

    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(20))
    model.add(Activation('relu'))
    model.add(Dense(20))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions))
    model.add(Activation('tanh'))
    # model.add(Dense(nb_actions))
    # model.add(Activation('linear'))
    print(model.summary())

    action_input = Input(shape=(nb_actions,), name='action_input')
    observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
    flattened_observation = Flatten()(observation_input)
    x = Concatenate()([action_input, flattened_observation])
    x = Dense(20)(x)
    x = Activation('tanh')(x)
    x = Dense(20)(x)
    x = Activation('relu')(x)
    x = Dense(1)(x)
    x = Activation('tanh')(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)
    print(critic.summary())
    memory = SequentialMemory(limit=20000, window_length=1)
    random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=0.6, mu=0, sigma=0.2)
    agent = DDPGAgent(nb_actions=nb_actions, actor=model, critic=critic, critic_action_input=action_input,
                      memory=memory, nb_steps_warmup_critic=1200, nb_steps_warmup_actor=1200,
                      random_process=random_process, memory_interval=32, gamma=4, target_model_update=1e-3)
    agent.compile(Adam(lr=0.0005, clipnorm=1.), metrics=['mae'])

    return agent
