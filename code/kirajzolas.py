import math
import os
import pygame

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

# variables
tracks = [[] for i in range(2)]

pygame.init()
Display = pygame.display.set_mode((900,900))
Display.fill(black)
currentTrackIndex=0

def drawPalya(x,y,Dir):
    Display.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.draw.polygon(Display, red, tracks[currentTrackIndex].inner, 3)
    pygame.draw.polygon(Display, red, tracks[currentTrackIndex].outer, 3)
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
                 (x+math.sin(dir+SearchLineAngles[i])*SearchLineDistances[i],
                  y+math.cos(dir+SearchLineAngles[i])*SearchLineDistances[i]))
        '''pygame.draw.circle(Display,white,(int(x+math.sin(dir+SearchLineAngles[i])*SearchLineDistances[i]),
                                         int(y+math.cos(dir+SearchLineAngles[i])*SearchLineDistances[i])),4)'''

class Track():
    def __init__(self):
        self.inner=[]
        self.outer=[]
        self.startPos = [100,100]
        self.startDir = 0.5

def getTracks(x = 0):
    filenames = os.listdir(os.getcwd() + "\\pontok")
    global tracks
    tracks=[]
    for file in filenames:
        tracks.append(Track())

    for i in range(len(filenames)):
        outerReady=False
        innerReady = False
        startReady = False
        f=open(os.getcwd()+"\\pontok\\"+filenames[i],"r")
        for line in f:
            if not outerReady:
                if line == "---\n":
                    outerReady = True
                else:
                    strings=line.split(",")
                    tracks[i].outer.append([int(strings[0]), int(strings[1])])
            elif not innerReady:
                if line == "---\n":
                    innerReady = True
                else:
                    strings = line.split(",")
                    tracks[i].inner.append([int(strings[0]), int(strings[1])])
            elif not startReady:
                if line == "---\n":
                    startReady = True
                else:
                    strings = line.split(",")
                    tracks[i].startPos = [int(strings[0]), int(strings[1])]
            else:
                strings = line.split(",")
                tracks[i].startDir = float(strings[0])

        f.close()
    return tracks[x]

def nextTrackIndex():       #lépteti a pályát, biztonságosan
    global currentTrackIndex
    if currentTrackIndex == len(tracks)-1:
        currentTrackIndex = 0
    else:
        currentTrackIndex = currentTrackIndex + 1
    return currentTrackIndex
