import kirajzolas
import physics
import math
import numpy as np

def calcDistances(x,y,dir):
    angles=kirajzolas.SearchLineAngles
    for i in range(len(angles)):
        kirajzolas.SearchLineDistances[i]=calcdist((x,y),(math.sin(dir+angles[i]),math.cos(dir+angles[i])))

def normalize(a):
    return a[0] / math.sqrt(a[0] * a[0] + a[1] * a[1]), a[1] / math.sqrt(a[0] * a[0] + a[1] * a[1])


def solvelineqsys(o, v, p1, p2):
    val = [10000, 10000]
    pv = (p2[0] - p1[0], p2[1] - p1[1])
    pv = normalize(pv)

    if (v[0] * pv[1] - v[1] * pv[0]) != 0:
        a = v[1] * o[0] - v[0] * o[1]
        b = pv[1] * p1[0] - pv[0] * p1[1]

        C = np.array([a,b])
        D = np.array([[v[1], -v[0]], [pv[1], -pv[0]]])
        mxy = np.linalg.solve(D, C)
        mv = ((mxy[0] - o[0]), (mxy[1] - o[1]))

        nvx, nvy = normalize(v)
        nmvx, nmvy = normalize(mv)

        if abs(nvx - nmvx) < 0.000001 and abs(nvy - nmvy) < 0.000001 and (
            min(p1[0], p2[0]) <= mxy[0] <= max(p1[0], p2[0])) and (min(p1[1], p2[1]) <= mxy[1] <= max(p1[1], p2[1])):
            val[0] = mxy[0]
            val[1] = mxy[1]
    else:
        pass
    return val


def calcdist(o, v):
    m1 = []
    # Calculate distance between car and inner side of the track
    for i in range(len(kirajzolas.palya_1b)):
        if i != len(kirajzolas.palya_1b) - 1:
            m1.append(solvelineqsys(o, v, kirajzolas.palya_1b[i], kirajzolas.palya_1b[i + 1]))

        else:
            m1.append(solvelineqsys(o, v, kirajzolas.palya_1b[i], kirajzolas.palya_1b[0]))

    for i in range(len(kirajzolas.palya_1k)):
        if i != len(kirajzolas.palya_1k) - 1:
            m1.append(solvelineqsys(o, v, kirajzolas.palya_1k[i], kirajzolas.palya_1k[i + 1]))

        else:
            m1.append(solvelineqsys(o, v, kirajzolas.palya_1k[i], kirajzolas.palya_1k[0]))

    valmin = (10000, 10000)
    for i in m1:
        if math.dist(o, i) < math.dist(o, valmin):
             valmin = i
    dist = math.dist(valmin, o)
    if dist <= physics.track:
        physics.collision = True
    return dist
