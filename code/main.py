import kirajzolas
from kisauto_env import Kisauto
from learning_models import ddpg_adam_ornstein

kirajzolas.init_searchlines(9)     # érzékelő vonalak megadása
kirajzolas.getTracks()              # betöltjük listába txt-ből a pályákat
env = Kisauto()                     # létrehozzuk a tesztkörnyezetet
ddpg_adam_ornstein.training(env)    # training algoritmus, scriptben paraméterezhető