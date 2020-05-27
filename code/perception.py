import map
import math
import numpy as np


# create array of distances for all searchlines
def calcDistances(env):
    angles = env.SearchLineAngles
    dists = [0 for i in range(len(angles))]
    belso = map.tracks[map.currentTrackIndex].inner
    kulso = map.tracks[map.currentTrackIndex].outer
    for i in range(len(angles)):
        dists[i] = calcdist((env.x, env. y), (math.sin(env.direction+angles[i]),
                                                 math.cos(env.direction+angles[i])), belso, kulso,env)
    env.SearchLineDistances=dists
    return dists


# calculate the distance sensed by one searchline
def calcdist(o, v, belso, kulso,env):
    m1 = []
    # Calculate distance between car and inner side of the track
    for i in range(len(belso)):
        if i != len(belso) - 1:
            m1.append(solvelineqsys(o, v, belso[i], belso[i + 1]))

        else:
            m1.append(solvelineqsys(o, v, belso[i], belso[0]))

    # Calculate distance between car and outer side of the track
    for i in range(len(kulso)):
        if i != len(kulso) - 1:
            m1.append(solvelineqsys(o, v, kulso[i], kulso[i + 1]))

        else:
            m1.append(solvelineqsys(o, v, kulso[i], kulso[0]))

    # minimal distance
    mindistance=2000
    for i in m1:
        if 0 < i < mindistance:
           mindistance = i
    if mindistance <= env.trackWidth or mindistance>1000:
        env.collision = True
    return mindistance


def normalize(a):
    return a[0] / math.sqrt(a[0] * a[0] + a[1] * a[1]), a[1] / math.sqrt(a[0] * a[0] + a[1] * a[1])

# calculate distance of one segment on one searchline
def solvelineqsys(o, v, p1, p2):
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

        if (min(p1[0], p2[0]) <= mxy[0] <= max(p1[0], p2[0])) and (min(p1[1], p2[1]) <= mxy[1] <= max(p1[1], p2[1])):
            if abs(nvx - nmvx) < 0.000001:
                min_dist = math.sqrt((mxy[0] - o[0]) * (mxy[0] - o[0]) + (mxy[1] - o[1]) * (mxy[1] - o[1]))
            else:
                min_dist = -math.sqrt((mxy[0] - o[0]) * (mxy[0] - o[0]) + (mxy[1] - o[1]) * (mxy[1] - o[1]))
    else:
        pass
    return min_dist


# calculate how parallel the car stands with the track
def performance(env):
    pos = np.array([env.x, env.y])
    belso = map.tracks[map.currentTrackIndex].inner
    kulso = map.tracks[map.currentTrackIndex].outer
    pclosest1=closestPoint(pos,  np.array(belso[len(belso)-1]), np.array(belso[0]))
    mindist1=np.sum((pclosest1-pos)**2)
    for i in range(len(belso)-1):
        p = closestPoint(pos, np.array(belso[i]), np.array(belso[i+1]))
        dist = np.sum((p - pos) ** 2)
        if dist<mindist1:
            mindist1=dist
            pclosest1=p
    pclosest2 = closestPoint(pos, np.array(kulso[len(kulso)-1]), np.array(kulso[0]))
    mindist2 = np.sum((pclosest2-pos)**2)
    for i in range(len(kulso) - 1):
        p = closestPoint(pos, np.array(kulso[i]), np.array(kulso[i+1]))
        dist = np.sum((p - pos) ** 2)
        if dist < mindist2:
            mindist2 = dist
            pclosest2 = p
    d = np.linalg.norm(pclosest1-pclosest2)
    return 1-abs(np.dot([math.sin(env.direction), math.cos(env.direction)], pclosest2-pclosest1)/d)


# closest point of line segment to the car
def closestPoint(pos, p1, p2):
    dirvec = np.array(p2-p1, dtype=np.float32)
    delta = np.linalg.norm(dirvec)
    dirvec = dirvec/delta
    from_start = pos-p1
    l = np.dot(dirvec,from_start)
    if l > delta:
        return p2
    elif l < 0:
        return p1
    else:
        return p1+l*dirvec
