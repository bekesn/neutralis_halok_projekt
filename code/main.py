import physics
import kirajzolas
import perception
import pygame

t = kirajzolas.getTracks(1)
x = t.startPos[0]
y = t.startPos[1]
Dir = t.startDir
speed = 0.0     # A sebesség változtatásához
skid = 0.0  # A csúszáshoz
skid_factor = 5     # Megadja, mennyivel változzon a csúszás értéke
kirajzolas.palya_1k=t.outer
kirajzolas.palya_1b=t.inner


def manual_steering():
    turn = 0.0
    dspeed = 0.0
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        turn = 0.4
    if pressed[pygame.K_RIGHT]:
        turn = -0.4
    if pressed[pygame.K_UP]:
        dspeed = 0.01   # Sebesség növelése
    if pressed[pygame.K_DOWN]:
        dspeed = -0.01  # Sebesség csökkentése
    return turn, dspeed

while True:
    speed = speed + manual_steering()[1]    # Tényleges sebesség kiszámítása
    (x, y, Dir, skid) = physics.move(x, y, Dir, speed, manual_steering()[0], skid)
    skid = skid + speed * skid_factor   # Csúszás értékének meghatározása a sebesség függvényében
    perception.calcDistances(x, y, Dir)
    kirajzolas.drawPalya(x, y, Dir)

