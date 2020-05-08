import numpy as np
from keras import regularizers
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, Flatten, Input, Concatenate
from keras.optimizers import Adam

from rl.agents import DDPGAgent
from rl.memory import SequentialMemory, EpisodeParameterMemory
from rl.random import OrnsteinUhlenbeckProcess
from datetime import datetime

import kirajzolas


def training(env):
    agent = create_agent(env)

    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    agent.fit(env, nb_steps=20000, nb_max_start_steps=4, action_repetition=1, nb_max_episode_steps=500, visualize=False, verbose=2)

    # After training is done, we save the best weights.
    time = datetime.now().strftime("%m%d_%H%M%S")
    agent.actor.save('models\\ddpg_keras_'+time+'.h5')
    agent.critic.save('models\\ddpg_keras_'+time+'_critic.h5')
    testing(env, time)
    # Finally, evaluate our algorithm for 5 episodes.

def testing(env, name):
    model = load_model("models\\ddpg_keras_"+name+'.h5')
    print(model.summary())

    obs = env.reset()
    observ = np.zeros((1,1,len(kirajzolas.SearchLineAngles)+1))
    round = 0
    print("\nTesting for", len(kirajzolas.tracks), "episodes:\n")
    while round < len(kirajzolas.tracks):
        observ[0] = obs
        [action] = model.predict(observ, batch_size=1)
        obs, rewards, done, info = env.step(action)
        env.render()
        if done or env.steps >= 1000:
            print("Episode", round+1, "ended in:", env.steps, "steps")
            env.reset()
            round += 1


def create_agent(env):
    np.random.seed(123)
    env.seed(None)

    nb_actions = env.action_space.shape[0]

    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(350,activity_regularizer=regularizers.l2(0.08)))
    #model.add(Activation('linear'))
    #model.add(Dense(60,activity_regularizer=regularizers.l2(0.08)))
    model.add(Activation('tanh'))
    model.add(Dense(nb_actions,activity_regularizer=regularizers.l2(0.08)))
    model.add(Activation('tanh'))
    # model.add(Dense(nb_actions))
    # model.add(Activation('linear'))
    print(model.summary())

    action_input = Input(shape=(nb_actions,), name='action_input')
    observation_input = Input(shape=(1,) + env.observation_space.shape, name='observation_input')
    flattened_observation = Flatten()(observation_input)
    x = Concatenate()([action_input, flattened_observation])
    x = Dense(50)(x)
    x = Activation('relu')(x)
    x = Dense(50)(x)
    x = Activation('tanh')(x)
    x = Dense(1)(x)
    x = Activation('tanh')(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)
    print(critic.summary())
    memory = SequentialMemory(limit=100000, window_length=1)
    random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.6 ,sigma_min=0.05,n_steps_annealing=12000)
    agent = DDPGAgent(nb_actions=nb_actions, actor=model, critic=critic, critic_action_input=action_input,
                      memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=4000,
                      random_process=random_process, gamma=.99, target_model_update=9e-4)
    agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])  # ezek a paraméterek nem kellenek

    return agent
