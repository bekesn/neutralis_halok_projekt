import map
from matchbox_env import Matchbox
import perception
import pygame

# checking keyboard input
def manual_steering():
    turn = 0.0
    dspeed = 0.0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        turn = 0.4
    if pressed[pygame.K_RIGHT]:
        turn = -0.4
    if pressed[pygame.K_UP]:
        dspeed = 0.01
    if pressed[pygame.K_DOWN]:
        dspeed = -0.01
    return dspeed,turn

# init tracks and car
map.getTracks()
env=Matchbox(9)
env.reset()

while True:
    if env.collision:
        env.reset()         # restarting on a different track
    control=manual_steering()
    env.move(control[0],control[1])
    perception.calcDistances(env)
    #perception.performance(env)
    env.render()



