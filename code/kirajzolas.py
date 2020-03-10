import pygame
import math

#constants

a = 10
b = 20
SearchLineAngles = [-math.pi/2,-math.pi*3/8,-math.pi/4,-math.pi*1/8,0.0,math.pi/8,math.pi/4,
                  math.pi*3/8,math.pi/2]
SearchLineDistances = [10,10,10,20,30,10,30,20,40]
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

palya_1b=[]
palya_1b.append((200,200))
palya_1b.append((200,400))
palya_1b.append((400,400))
palya_1b.append((400,200))

palya_1k=[]
palya_1k.append((100,100))
palya_1k.append((100,500))
palya_1k.append((700,500))
palya_1k.append((700,100))

pygame.init()
Display = pygame.display.set_mode((900,900))
Display.fill(black)

def drawPalya(x,y,Dir):
    Display.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.draw.polygon(Display, red, palya_1b, 3)
    pygame.draw.polygon(Display, red, palya_1k, 3)
    drawSearchLine(x,y,Dir)
    pygame.draw.polygon(Display, green, (
        (int(x + a * math.cos(Dir) - b * math.sin(Dir)), int(y - a * math.sin(Dir) - b * math.cos(Dir))),
        (int(x + a * math.cos(Dir) + b * math.sin(Dir)), int(y - a * math.sin(Dir) + b * math.cos(Dir))),
        (int(x - a * math.cos(Dir) + b * math.sin(Dir)), int(y + a * math.sin(Dir) + b * math.cos(Dir))),
        (int(x - a * math.cos(Dir) - b * math.sin(Dir)), int(y + a * math.sin(Dir) - b * math.cos(Dir)))))
    pygame.display.update()

def drawSearchLine(x,y,dir):
    for i in range(len(SearchLineAngles)):
        pygame.draw.line(Display,blue,(x,y),
                 (x+math.sin(dir+SearchLineAngles[i])*500,y+math.cos(dir+SearchLineAngles[i])*500))
        pygame.draw.circle(Display,white,(int(x+math.sin(dir+SearchLineAngles[i])*SearchLineDistances[i]),
                                         int(y+math.cos(dir+SearchLineAngles[i])*SearchLineDistances[i])),4)