import kirajzolas
from kisauto_env import Kisauto
from learning_models import ddpg_adam_ornstein,ddpg_stable

kirajzolas.init_searchlines(15)     # érzékelő vonalak megadása
kirajzolas.getTracks()              # betöltjük listába txt-ből a pályákat
env = Kisauto()                     # létrehozzuk a tesztkörnyezetet
#ddpg_adam_ornstein.training(env)    # training algoritmus, scriptben paraméterezhető
ddpg_adam_ornstein.testing(env, 'slip_jo')
#ddpg_stable.training(env)
#ddpg_stable.testing(env, 'proba')