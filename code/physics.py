import math
# constants describing physics
wheelBase = 20
track = 10
slipEnabled = True  # False / True
slipLimit = 0.004
turnLimit = 0.3   # math.pi/4
g = 9.81
mu = 1.5  # Tapadási súrlódási tényező
px = 5  # px/s to m/s
pr = 10  # m to px
rand=10
skid_factor=4 # Megadja, mennyivel változzon a csúszás értéke
max_accelerating=0.05
speedlimit = 4

# status
slip = 0
collision = False
skid=0.0
speed=0.0
performance=1
turn=0.0
throttle=0.0
direction=0.0

def reset():
    global slip
    global collision
    global skid
    global speed
    global turn
    global  throttle
    slip = 0
    collision=False
    skid=0.0
    speed=0.0
    turn=0.0
    throttle=0.0


def move(x, y, dir, speedChange, dirChange):
    global skid # így lehet elérni őket függvényben
    global slip
    global speed
    global turn
    global throttle
    global direction
    direction=dir
    throttle=speedChange
    if -speedlimit < speed + speedChange < speedlimit:
        speed = speed + speedChange  # jelenlegi sebesség
    elif speed < -speedlimit:
        speed = -speedlimit
    else:
        speed = speedlimit
    slip = 0
    if dirChange == 0:
        x = x + math.sin(dir) * speed
        y = y + math.cos(dir) * speed
        skid = 0.0  # Ebben az esetben nem csúszik az autó
    else:
        dirChange = min(dirChange, turnLimit)
        dirChange = max(dirChange, -turnLimit)
        rad = wheelBase / math.tan(dirChange)
        rad = math.sqrt(rad * rad + wheelBase * wheelBase / 4) * dirChange / abs(dirChange)
        origo = (x + math.cos(dir) * rad, y - math.sin(dir) * rad)
        v_max = math.sqrt(g * mu * abs(rad / pr))
        rad_min = speed * speed * px * px * pr / (g * mu)
        if slipEnabled and speed * px > v_max:

            if abs(rad) + skid < rad_min:   # Addig növeljük a csúszás értékét, amíg a megfelelő körpályára kerül
                mrad = rad / (abs(rad) + skid)
            else:
                mrad = rad / rad_min
                skid = rad_min - abs(rad) + 10  # Amint a megfelelő körpályán vagyunk, nem változik az értéke. 10 := biztonsági tényező
            # print(v_max, rad, rad_min, skid, mrad)
            x = x + math.sin(dir) * speed
            y = y + math.cos(dir) * speed
            dir = dir + speed / rad * abs(mrad)   # Ezzel a képlettel adjuk meg a csúszás mértékét
            slip=1-abs(mrad)
        else:
            skid = 0.0  # Ebben az esetben nem csúszik az autó
            dir = dir + speed / rad
            x = origo[0] - math.cos(dir) * rad
            y = origo[1] + math.sin(dir) * rad
    skid = skid + abs(speed) * skid_factor  # Csúszás értékének meghatározása a sebesség függvényében
    turn = dirChange
    return (x, y, dir, collision)
