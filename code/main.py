import map
from matchbox_env import Matchbox
from learning_models import ddpg_keras,ddpg_stable


# The maps will be loaded as .txt files from the test or train folders
map.getTracks()

# Generating the custom environment
# It has to be initialized with the number of searching lines
# Its value has to be changed according to the model
# Values: 3 5 9 15 20 25 40
env = Matchbox(9)

# Pre-trained models using the DDPG algorithm
# In order to use the models, please, uncomment the desired models and comment out the unused ones
# Most models were named after their structure in the form of kx_ly_nz1_z2_z3_...,
# Where k means the searching lines and its number is x,
# l means the layers without the output and its number is y and
# n means the neurons in each layer, except the output layer, where z1, z2, z3... are the numbers of neurons

#######################################################################################################################
# Models without the slip effect
# Please, set the "env.slipEnabled" to "False"
env.slipEnabled = False

# This trained network achieved the best results both in training and testing
ddpg_keras.testing(env, 'k9_best_nn')

# This model was the first example in the presentation
#ddpg_keras.testing(env, 'k5_l3_n200_300_200')

# This model was the second example in the presentation
#ddpg_keras.testing(env, 'k15_l6_n100_200_300_200_100_100')

# This model was the third example in the presentation
#ddpg_keras.testing(env, 'k40_l2_n100')

# This is a random model
#ddpg_keras.testing(env, 'k25_l3_n200_300_200')

#######################################################################################################################
# Models with the slip effect
# Please, set the "env.slipEnabled" to "True"
#env.slipEnabled = True

# First model handling the slip effect
#ddpg_keras.testing(env, 'wslip_k9_m1')

# Second model handling the slip effect
#ddpg_keras.testing(env, 'wslip_k9_m2')

# Third model handling the slip effect
#ddpg_keras.testing(env, 'wslip_k9_m3')

#######################################################################################################################
# Training the DDPG algorithm
# Its parameters can be set in the "ddpg_keras.py" file, in the "training()" function

#ddpg_keras.training(env)

#######################################################################################################################
# Training & testing models using DDPG Stable Baseline algorithm

#ddpg_stable.training(env)

#ddpg_stable.testing(env, 'test')
