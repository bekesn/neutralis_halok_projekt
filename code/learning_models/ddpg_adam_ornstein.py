import numpy as np
from keras import regularizers
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory, EpisodeParameterMemory
from rl.random import OrnsteinUhlenbeckProcess
from datetime import datetime

def training(env):
    agent = create_agent(env)

    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    agent.fit(env, nb_steps=16000, nb_max_start_steps=5, action_repetition=1, nb_max_episode_steps=800, visualize=True, verbose=2)

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
    model.add(Dense(40,activity_regularizer=regularizers.l2(0.05)))
    model.add(Activation('linear'))
    model.add(Dense(40,activity_regularizer=regularizers.l2(0.05)))
    model.add(Activation('sigmoid'))
    model.add(Dense(10,activity_regularizer=regularizers.l2(0.05)))
    model.add(Activation('relu'))
    model.add(Dense(nb_actions,activity_regularizer=regularizers.l2(0.05)))
    model.add(Activation('tanh'))
    # model.add(Dense(nb_actions))
    # model.add(Activation('linear'))
    print(model.summary())

    action_input = Input(shape=(nb_actions,), name='action_input')
    observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
    flattened_observation = Flatten()(observation_input)
    x = Concatenate()([action_input, flattened_observation])
    x = Dense(40)(x)
    x = Activation('relu')(x)
    x = Dense(40)(x)
    x = Activation('relu')(x)
    x = Dense(10)(x)
    x = Activation('tanh')(x)
    x = Dense(1)(x)
    x = Activation('sigmoid')(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)
    print(critic.summary())
    memory = SequentialMemory(limit=2000, window_length=1)
    random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=0.6, mu=0., sigma=0.4, sigma_min=0.01, n_steps_annealing=4000)
    agent = DDPGAgent(nb_actions=nb_actions, actor=model, critic=critic, critic_action_input=action_input, batch_size=64,
                      memory=memory, nb_steps_warmup_critic=4000, nb_steps_warmup_actor=4000,
                      random_process=random_process, memory_interval=1, gamma=0.99, target_model_update=0.001)
    agent.compile(Adam(lr=0.005, clipnorm=1.), metrics=['mae'])  # ezek a paraméterek nem kellenek

    return agent
