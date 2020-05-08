import kirajzolas
import physics
import perception
import pygame

kirajzolas.init_searchlines(9)
kirajzolas.getTracks()
x = kirajzolas.tracks[kirajzolas.currentTrackIndex].startPos[0]
y = kirajzolas.tracks[kirajzolas.currentTrackIndex].startPos[1]
Dir = kirajzolas.tracks[kirajzolas.currentTrackIndex].startDir


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
    if physics.collision:       #ilyenkor újraindulunk egy másik pályán
        physics.reset()
        i = kirajzolas.nextTrackIndex()
        x = kirajzolas.tracks[i].startPos[0]
        y = kirajzolas.tracks[i].startPos[1]
        Dir = kirajzolas.tracks[i].startDir
    (x, y, Dir, skid) = physics.move(x, y, Dir, manual_steering()[1], manual_steering()[0])
    perception.calcDistances(x,y,Dir)
    perception.calcDistances(x, y, Dir)
    kirajzolas.drawPalya(x, y, Dir)

