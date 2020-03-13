import physics
import kirajzolas
import perception
import pygame

t = kirajzolas.getTracks(1)
x = t.startPos[0]
y = t.startPos[1]
Dir = t.startDir
kirajzolas.palya_1k=t.outer
kirajzolas.palya_1b=t.inner


def manual_steering():
    turn = 0.0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        turn = 0.3
    if pressed[pygame.K_RIGHT]:
        turn = -0.3
    return turn

while True:
    (x, y, Dir) = physics.move(x, y, Dir, 0.5, manual_steering())
    perception.calcDistances(x, y, Dir)
    kirajzolas.drawPalya(x, y, Dir)

