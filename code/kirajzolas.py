import math
import os
import pygame
import physics
import perception

#constants

a = 10
b = 20
SearchLineAngles = []

white = (255,255,255)
black = (0,0,0)
red = (100,0,0)
green = (0,200,0)
blue = (0,0,100)

# variables
tracks = [[] for i in range(2)]
SearchLineDistances = []
currentTrackIndex=0

pygame.init()
Display = pygame.display.set_mode((900,650))
Display.fill(black)


def drawPalya(x,y,Dir):
    Display.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(1)
    drawStatus()
    pygame.draw.polygon(Display, red, tracks[currentTrackIndex].inner, 3)
    pygame.draw.polygon(Display, red, tracks[currentTrackIndex].outer, 3)
    #drawSearchLine(x,y,Dir)
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
    #[p1, p2]=perception.centerized(x,y)
    #print(p1)
    #pygame.draw.circle(Display,white,(int(p1[0]),int(p1[1])),4)
    #pygame.draw.circle(Display, white, (int(p2[0]), int(p2[1])), 4)


def drawStatus():
    size=40
    if physics.speed>0:
        vel=int((physics.throttle/2+0.5)*size)#round(physics.speed / physics.speedlimit * size)
        Display.fill([200, 200, 0], (0, 0, size, size-vel))
        Display.fill([0,200,200], (0, size-vel, size, vel))
    else:
        Display.fill([255, 0, 0], (0, 0, size, size))
    turn = int((physics.turn/physics.turnLimit+1)/2*size)
    Display.fill([0, 0, 255], (size, 0, size-turn, size))
    Display.fill([0, 255, 0], (2*size-turn, 0, turn, size))
    Display.fill([255*physics.slip, 0, 0], (2*size, 0, size, size))


class Track():
    def __init__(self):
        self.inner=[]
        self.outer=[]
        self.startPos = [100,100]
        self.startDir = 0.5


def getTracks(x = 0, type="train"):
    if type=="train":
        filenames = os.listdir(os.getcwd() + "\\train")
    elif type=="test":
        filenames = os.listdir(os.getcwd() + "\\test")
    else:
        print("Wrong track type. Allowed: train/test")
        quit(2);
    global tracks
    tracks=[]
    for file in filenames:
        tracks.append(Track())

    for i in range(len(tracks)):
        outerReady=False
        innerReady = False
        startReady = False
        f=open(os.getcwd()+"\\"+type+"\\"+filenames[i],"r")
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
    if currentTrackIndex >= len(tracks)-1:
        currentTrackIndex = 0
    else:
        currentTrackIndex = currentTrackIndex + 1
    return currentTrackIndex


def init_searchlines(n, angle1=-math.pi/2, angle2=math.pi/2): # n vonal, szögtartomány: angle1-től angle2-ig
    global SearchLineAngles
    global SearchLineDistances
    SearchLineDistances = [0 for i in range(n)]
    SearchLineAngles = [0 for i in range(n)]
    for i in range(n):
        SearchLineAngles[i] = angle1+(angle2-angle1)*float(i)/float(n-1)