import pygame
import math

pygame.init()

white = (255,255,255)
black = (0,0,0)

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

Display = pygame.display.set_mode((800,600))
Display.fill(black)
a=10
b=20
x=100
y=200
Dir=0
while True:
    Display.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    Dir = Dir + 0.001
    pygame.draw.polygon(Display,green,((int(x+a*math.cos(Dir)-b*math.sin(Dir)),int(y-a*math.sin(Dir)-b*math.cos(Dir))),
                (int(x + a * math.cos(Dir) + b * math.sin(Dir)), int(y - a * math.sin(Dir) + b * math.cos(Dir))),
                (int(x - a * math.cos(Dir) + b * math.sin(Dir)), int(y + a * math.sin(Dir) + b * math.cos(Dir))),
                (int(x - a * math.cos(Dir) - b * math.sin(Dir)), int(y + a * math.sin(Dir) - b * math.cos(Dir)))))
    pygame.display.update()
