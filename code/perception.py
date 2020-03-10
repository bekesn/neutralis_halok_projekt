import kirajzolas
import math

def calcDistances(x,y,dir):
    angles=kirajzolas.SearchLineAngles
    for i in range(len(angles)):
        kirajzolas.SearchLineDistances[i]=calcDist(x,y,(math.sin(dir+angles[i]),math.cos(dir+angles[i])))

def calcDist(x,y,v):
    return(20)