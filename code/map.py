import math
import os
import pygame

#constants

white = (255,255,255)
black = (0,0,0)
red = (100,0,0)
green = (0,200,0)
blue = (0,0,100)

# variables
tracks = [[] for i in range(2)]
currentTrackIndex=0

pygame.init()
Display = pygame.display.set_mode((900,650))
Display.fill(black)

# updating display
def drawEnv(env):
    x = env.x
    y = env.y
    Dir = env.direction
    a = env.trackWidth
    b = env.wheelBase
    SearchLineAngles = env.SearchLineAngles
    SearchLineDistances = env.SearchLineDistances

    Display.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(1)

    drawStatus(env)
    pygame.draw.polygon(Display, red, tracks[currentTrackIndex].inner, 3)
    pygame.draw.polygon(Display, red, tracks[currentTrackIndex].outer, 3)
    drawSearchLine(x,y,Dir,SearchLineAngles, SearchLineDistances)
    pygame.draw.polygon(Display, green, (
        (int(x + a * math.cos(Dir) - b * math.sin(Dir)), int(y - a * math.sin(Dir) - b * math.cos(Dir))),
        (int(x + a * math.cos(Dir) + b * math.sin(Dir)), int(y - a * math.sin(Dir) + b * math.cos(Dir))),
        (int(x - a * math.cos(Dir) + b * math.sin(Dir)), int(y + a * math.sin(Dir) + b * math.cos(Dir))),
        (int(x - a * math.cos(Dir) - b * math.sin(Dir)), int(y + a * math.sin(Dir) - b * math.cos(Dir)))))
    pygame.display.update()


# drawing searchlines
def drawSearchLine(x,y,dir,SearchLineAngles,SearchLineDistances):
    for i in range(len(SearchLineAngles)):
        pygame.draw.line(Display,blue,(x,y),
                 (x+math.sin(dir+SearchLineAngles[i])*SearchLineDistances[i],
                  y+math.cos(dir+SearchLineAngles[i])*SearchLineDistances[i]))


# feedback on throttle, turn angle, and slip in the left upper corner
def drawStatus(env):
    size=40
    vel=int((env.throttle/2+0.5)*size)
    Display.fill([200, 200, 0], (0, 0, size, size-vel))
    Display.fill([0,200,200], (0, size-vel, size, vel))
    turn = int((env.turn/env.turnLimit+1)/2*size)
    Display.fill([0, 0, 255], (size, 0, size-turn, size))
    Display.fill([0, 255, 0], (2*size-turn, 0, turn, size))
    Display.fill([255*env.slip, 0, 0], (2*size, 0, size, size))


class Track():
    def __init__(self):
        self.inner=[]
        self.outer=[]
        self.startPos = [100,100]
        self.startDir = 0.5

# load every track from train or test folder
def getTracks(type="train"):
    if type=="train":
        filenames = os.listdir(os.getcwd() + "\\train")
    elif type=="test":
        filenames = os.listdir(os.getcwd() + "\\test")
    else:
        print("Wrong track type. Allowed: train/test")
        quit(2)
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


# incrementing the index without indexing out
def nextTrackIndex():
    global currentTrackIndex
    if currentTrackIndex >= len(tracks)-1:
        currentTrackIndex = 0
    else:
        currentTrackIndex = currentTrackIndex + 1
    return currentTrackIndex
