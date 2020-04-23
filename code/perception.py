import kirajzolas
import physics
import math
import numpy as np


def calcDistances(x, y, dir):       #autó helyzetének 3 paramétere, pálya indexe
    angles = kirajzolas.SearchLineAngles
    inputData = [0 for i in range(len(angles))]
    belso = kirajzolas.tracks[kirajzolas.currentTrackIndex].inner
    kulso = kirajzolas.tracks[kirajzolas.currentTrackIndex].outer
    for i in range(len(angles)):
        inputData[i] = calcdist((x, y), (math.sin(dir+angles[i]), math.cos(dir+angles[i])), belso, kulso)
    kirajzolas.SearchLineDistances=inputData
    return inputData

def normalize(a):
    return a[0] / math.sqrt(a[0] * a[0] + a[1] * a[1]), a[1] / math.sqrt(a[0] * a[0] + a[1] * a[1])


def solvelineqsys(o, v, p1, p2):
    #val = [10000, 10000]
    min_dist=2000
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

        # and abs(nvy - nmvy) < 0.000001 - ez nem kell, elég x-re tesztelni
        if (min(p1[0], p2[0]) <= mxy[0] <= max(p1[0], p2[0])) and (min(p1[1], p2[1]) <= mxy[1] <= max(p1[1], p2[1])):
            if abs(nvx - nmvx) < 0.000001:
                #val[0] = mxy[0]
                #val[1] = mxy[1]
                min_dist = math.sqrt((mxy[0] - o[0]) * (mxy[0] - o[0]) + (mxy[1] - o[1]) * (mxy[1] - o[1]))
            else:
                min_dist = -math.sqrt((mxy[0] - o[0]) * (mxy[0] - o[0]) + (mxy[1] - o[1]) * (mxy[1] - o[1]))
    else:
        pass
    return min_dist


def calcdist(o, v, belso, kulso):
    m1 = []
    # Calculate distance between car and inner side of the track
    for i in range(len(belso)):
        if i != len(belso) - 1:
            m1.append(solvelineqsys(o, v, belso[i], belso[i + 1]))

        else:
            m1.append(solvelineqsys(o, v, belso[i], belso[0]))

    for i in range(len(kulso)):
        if i != len(kulso) - 1:
            m1.append(solvelineqsys(o, v, kulso[i], kulso[i + 1]))

        else:
            m1.append(solvelineqsys(o, v, kulso[i], kulso[0]))

    mindistance=2000
    for i in m1:
        #d=math.sqrt((i[0] - o[0]) * (i[0] - o[0]) + (i[1] - o[1]) * (i[1] - o[1]))
        if 0<i<mindistance:
           mindistance=i
    if mindistance <= physics.track or mindistance>1000:
        physics.collision = True
    return mindistance
